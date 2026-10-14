#!/usr/bin/env python3
"""Receptor local de la telemetría de Claude Code (OTLP por HTTP con JSON).

Escucha solo en 127.0.0.1 y guarda cada evento (`api_request`, `tool_result`, `user_prompt`...) como una línea JSON
plana en `<carpeta>/AAAA-MM-DD.jsonl`, con los atributos del recurso (entre ellos `tarea.id` y `kit.version`) ya
mezclados. Antes de escribir borra los atributos que pueden llevar datos del cliente: parámetros de herramientas,
comandos de Bash, texto de prompts y respuestas, y mensajes de error completos.

Las métricas y las trazas se aceptan y se descartan: el script de métricas trabaja solo con los eventos.

Uso:
    python3 receptor_telemetria.py                       # puerto 4318, carpeta ~/.kit-agentes/telemetria
    python3 receptor_telemetria.py --puerto 4319 --carpeta /tmp/telemetria

Solo usa la biblioteca estándar. No envía nada a ningún sitio.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Atributos que pueden contener código, comandos, rutas o texto del cliente. Nunca se guardan.
ATRIBUTOS_BORRADOS = {
    "tool_parameters", "tool_input", "tool.output", "prompt", "prompt_text", "response", "error",
    "workspace.host_paths", "user.email",
}
TAMANO_MAXIMO = 20 * 1024 * 1024  # una petición OTLP normal ocupa unos pocos KB
BLOQUEO = threading.Lock()
MARCA = "kit-agentes-telemetria"  # lo que responde /salud; lanzar.sh lo comprueba


def leer_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--puerto", type=int, default=4318)
    p.add_argument("--carpeta", default=str(Path.home() / ".kit-agentes" / "telemetria"))
    return p.parse_args()


def valor(v: dict):
    """Valor de un AnyValue de OTLP en JSON."""
    if "stringValue" in v:
        return v["stringValue"]
    if "intValue" in v:
        return int(v["intValue"])
    if "doubleValue" in v:
        return float(v["doubleValue"])
    if "boolValue" in v:
        return bool(v["boolValue"])
    if "arrayValue" in v:
        return [valor(x) for x in v["arrayValue"].get("values", [])]
    if "kvlistValue" in v:
        return atributos(v["kvlistValue"].get("values", []))
    return None


def atributos(lista: list[dict]) -> dict:
    return {a["key"]: valor(a.get("value") or {}) for a in lista or [] if "key" in a}


def eventos(cuerpo: dict):
    for recurso_logs in cuerpo.get("resourceLogs", []):
        recurso = atributos((recurso_logs.get("resource") or {}).get("attributes", []))
        for ambito in recurso_logs.get("scopeLogs", []):
            for registro in ambito.get("logRecords", []):
                evento = {**recurso, **atributos(registro.get("attributes", []))}
                if "event.name" not in evento:
                    cuerpo_registro = valor(registro.get("body") or {})
                    if isinstance(cuerpo_registro, str):
                        evento["event.name"] = cuerpo_registro.removeprefix("claude_code.")
                for clave in ATRIBUTOS_BORRADOS & evento.keys():
                    del evento[clave]
                yield evento


class Manejador(BaseHTTPRequestHandler):
    carpeta: Path

    def do_GET(self) -> None:  # noqa: N802 (nombre impuesto por http.server)
        # El lanzador comprueba aquí que el puerto es de este receptor y no de otro colector.
        if self.path.rstrip("/") != "/salud":
            self.responder(404, "No existe")
            return
        cuerpo = json.dumps({"servicio": MARCA}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_POST(self) -> None:  # noqa: N802 (nombre impuesto por http.server)
        longitud = int(self.headers.get("Content-Length") or 0)
        if longitud > TAMANO_MAXIMO:
            self.responder(413)
            return
        datos = self.rfile.read(longitud)
        if self.path.rstrip("/") != "/v1/logs":
            self.responder(200)  # métricas y trazas: se aceptan y se descartan
            return
        if "json" not in (self.headers.get("Content-Type") or ""):
            self.responder(415, "Usa OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=http/json")
            return
        try:
            if (self.headers.get("Content-Encoding") or "").lower() == "gzip":
                datos = gzip.decompress(datos)
            filas = list(eventos(json.loads(datos)))
        except (OSError, ValueError) as error:
            self.responder(400, str(error))
            return
        self.guardar(filas)
        self.responder(200)

    def guardar(self, filas: list[dict]) -> None:
        if not filas:
            return
        ruta = self.carpeta / f"{datetime.now(timezone.utc):%Y-%m-%d}.jsonl"
        lineas = "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in filas)
        with BLOQUEO:
            descriptor = os.open(ruta, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            with os.fdopen(descriptor, "a", encoding="utf-8") as fichero:
                fichero.write(lineas)

    def responder(self, codigo: int, mensaje: str = "") -> None:
        cuerpo = json.dumps({"error": mensaje} if mensaje else {}).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, *args) -> None:  # sin ruido en la terminal
        pass


def main() -> None:
    args = leer_args()
    carpeta = Path(args.carpeta).expanduser()
    carpeta.mkdir(parents=True, exist_ok=True, mode=0o700)
    Manejador.carpeta = carpeta
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", args.puerto), Manejador)
    except OSError as error:
        sys.exit(f"No puedo escuchar en 127.0.0.1:{args.puerto}: {error}")
    print(f"Receptor de telemetría en http://127.0.0.1:{args.puerto}, guardando en {carpeta}", flush=True)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
