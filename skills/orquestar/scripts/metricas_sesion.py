#!/usr/bin/env python3
"""Métricas de una sesión de Claude Code a partir de su transcripción.

Lee la transcripción (`~/.claude/projects/<repo>/<sesión>.jsonl` y las de sus subagentes) y escribe un resumen
en Markdown y en JSON: tiempos, mensajes, herramientas, agentes, tokens por modelo y agente, y lo que habría
costado a precio de API.

Si la sesión se abrió con `lanzar.sh`, los tokens, el coste y el reparto por agente salen de la telemetría que
guardó el receptor local (`~/.kit-agentes/telemetria`), que tiene la salida real de cada llamada, subagentes
incluidos, y no depende de salir con `/exit`. Las transcripciones quedan para tiempos, mensajes y ficheros. El
nombre de la tarea se toma de `KIT_TAREA`, que pone el lanzador.

Uso:
    python3 metricas_sesion.py                                # tarea de KIT_TAREA, sesión más reciente del repo
    python3 metricas_sesion.py --slug research-llm            # sesión más reciente del repo actual
    python3 metricas_sesion.py --sesion <id o ruta> --repo ~/work/coop-investment-fund --slug x
    python3 metricas_sesion.py --desde 2026-10-13 --slug x     # todas las sesiones del repo desde esa fecha

Solo usa la biblioteca estándar. No envía nada a ningún sitio.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PAUSA_INACTIVA_S = 5 * 60  # huecos mayores no cuentan como tiempo activo
HERRAMIENTAS_EDICION = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
HERRAMIENTAS_AGENTE = {"Agent", "Task"}
# Mensajes de tipo "user" que escribe el propio Claude Code, no la persona.
PREFIJOS_ARNES = ("<system-reminder", "<local-command", "<task-notification", "<bash-", "<user-prompt-submit-hook",
                  "Caveat:", "[Request interrupted")


def leer_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", default=".", help="Directorio del repo donde se lanzó Claude Code (por defecto, el actual).")
    p.add_argument("--sesion", help="Id de la sesión o ruta al .jsonl. Por defecto, la más reciente del repo.")
    p.add_argument("--desde", help="Fecha AAAA-MM-DD: junta todas las sesiones del repo con actividad desde ese día.")
    p.add_argument("--slug", default=os.environ.get("KIT_TAREA") or "sesion",
                   help="Nombre corto de la tarea para los ficheros de salida (por defecto, KIT_TAREA).")
    p.add_argument("--telemetria", default=os.environ.get("KIT_TELEMETRIA") or str(Path.home() / ".kit-agentes" / "telemetria"),
                   help="Carpeta del receptor de telemetría. Si tiene eventos de la tarea, mandan sobre las transcripciones.")
    p.add_argument("--salida", help="Carpeta de salida. Por defecto, <repo>/.agentes/metricas.")
    p.add_argument("--precios", default=str(Path(__file__).with_name("precios.json")))
    p.add_argument("--projects", default=str(Path.home() / ".claude" / "projects"))
    return p.parse_args()


def carpeta_proyecto(projects: Path, repo: Path) -> Path:
    nombre = re.sub(r"[^A-Za-z0-9]", "-", str(repo))
    candidata = projects / nombre
    if candidata.is_dir():
        return candidata
    sys.exit(f"No encuentro la carpeta de transcripciones {candidata}. Usa --sesion con la ruta al .jsonl.")


def localizar_sesiones(args: argparse.Namespace) -> list[Path]:
    if args.sesion and args.sesion.endswith(".jsonl"):
        ruta = Path(args.sesion).expanduser()
        if not ruta.is_file():
            sys.exit(f"No existe la transcripción {ruta}.")
        return [ruta]
    carpeta = carpeta_proyecto(Path(args.projects).expanduser(), Path(args.repo).expanduser().resolve())
    if args.sesion:
        return [carpeta / f"{args.sesion}.jsonl"]
    ficheros = sorted(carpeta.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)
    if args.desde:
        limite = datetime.fromisoformat(args.desde).timestamp()
        ficheros = [f for f in ficheros if f.stat().st_mtime >= limite]
    elif ficheros:
        ficheros = ficheros[-1:]
    if not ficheros:
        sys.exit(f"No hay transcripciones en {carpeta}.")
    return ficheros


def leer_jsonl(ruta: Path) -> list[dict]:
    filas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        try:
            filas.append(json.loads(linea))
        except json.JSONDecodeError:
            continue
    return filas


def fecha(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def modelo_base(modelo: str) -> str:
    return re.sub(r"\[.*\]$", "", modelo or "desconocido")


def es_peticion_humana(fila: dict) -> bool:
    if fila.get("type") != "user" or fila.get("isMeta") or fila.get("isCompactSummary"):
        return False
    contenido = (fila.get("message") or {}).get("content")
    if isinstance(contenido, list):
        tipos = {b.get("type") for b in contenido if isinstance(b, dict)}
        if "tool_result" in tipos or "text" not in tipos:
            return False
    texto_fila = texto(fila).lstrip()
    return bool(texto_fila) and not texto_fila.startswith(PREFIJOS_ARNES)


def texto(fila: dict) -> str:
    contenido = (fila.get("message") or {}).get("content")
    if isinstance(contenido, str):
        return contenido
    return "".join(b.get("text", "") for b in contenido or [] if isinstance(b, dict) and b.get("type") == "text")


def coste(uso: dict, precio: dict | None) -> float | None:
    if precio is None:
        return None
    millon = 1_000_000
    entrada = precio["entrada"]
    return (
        uso["entrada"] * entrada
        + uso["salida"] * precio["salida"]
        + uso["lectura_cache"] * precio["lectura_cache"]
        + uso["escritura_cache_5m"] * entrada * 1.25
        + uso["escritura_cache_1h"] * entrada * 2
    ) / millon


def uso_vacio() -> dict:
    return {"llamadas": 0, "entrada": 0, "salida": 0, "razonamiento": 0, "lectura_cache": 0,
            "escritura_cache_5m": 0, "escritura_cache_1h": 0}


def sumar_uso(destino: dict, usage: dict) -> None:
    creacion = usage.get("cache_creation") or {}
    escritura_5m = creacion.get("ephemeral_5m_input_tokens")
    escritura_1h = creacion.get("ephemeral_1h_input_tokens")
    if escritura_5m is None and escritura_1h is None:
        escritura_5m, escritura_1h = usage.get("cache_creation_input_tokens", 0), 0
    destino["llamadas"] += 1
    destino["entrada"] += usage.get("input_tokens", 0)
    destino["salida"] += usage.get("output_tokens", 0)
    destino["razonamiento"] += (usage.get("output_tokens_details") or {}).get("thinking_tokens", 0)
    destino["lectura_cache"] += usage.get("cache_read_input_tokens", 0)
    destino["escritura_cache_5m"] += escritura_5m or 0
    destino["escritura_cache_1h"] += escritura_1h or 0


def nombre_subagente(ruta: Path) -> str:
    """Tipo de subagente si Claude Code lo guardó junto a su transcripción; si no, el nombre del fichero."""
    meta = ruta.with_suffix(".meta.json")
    if meta.is_file():
        try:
            datos = json.loads(meta.read_text(encoding="utf-8"))
            tipo = datos.get("agentType") or datos.get("subagent_type")
            if tipo:
                return f"{tipo} ({ruta.stem})"
        except json.JSONDecodeError:
            pass
    return ruta.stem


def analizar(principales: list[Path], precios: dict) -> dict:
    fuentes: list[tuple[str, Path]] = []
    for principal in principales:
        fuentes.append(("principal", principal))
        carpeta_sesion = principal.with_suffix("")
        if carpeta_sesion.is_dir():
            for f in sorted(carpeta_sesion.rglob("*.jsonl")):
                fuentes.append((nombre_subagente(f), f))

    # Claude Code guarda una fila por bloque de contenido y repite el uso en cada una; en algunas filas el
    # recuento de salida aún es parcial. Por cada petición a la API se queda la fila con más salida.
    llamadas: dict[str, tuple[str, str, dict, str | None]] = {}
    instantes: list[datetime] = []
    uso_por_modelo: dict[str, dict] = defaultdict(uso_vacio)
    uso_por_agente: dict[str, dict] = defaultdict(uso_vacio)
    herramientas: Counter = Counter()
    errores_herramientas = 0
    subagentes: Counter = Counter()
    skills: Counter = Counter()
    ficheros_editados: set[str] = set()
    esfuerzos: Counter = Counter()
    compactaciones = 0
    peticiones: list[dict] = []
    estados_coste: dict[int, dict] = {}
    meta: dict = {}
    sesiones: list[str] = []
    ultimo_asistente: datetime | None = None

    for agente, ruta in fuentes:
        if agente == "principal":
            ultimo_asistente = None
        filas = leer_jsonl(ruta)
        for fila in filas:
            if fila.get("type") == "cost-state":
                estados_coste[(fila.get("sessionId"), fila.get("startTime", 0))] = fila
                continue
            if fila.get("type") == "system" and fila.get("subtype") == "compact_boundary":
                compactaciones += 1
            instante = fecha(fila.get("timestamp"))
            if instante:
                instantes.append(instante)
            if agente == "principal" and fila.get("sessionId") and fila["sessionId"] not in sesiones:
                sesiones.append(fila["sessionId"])
            if agente == "principal" and not meta and fila.get("cwd"):
                meta = { "cwd": fila.get("cwd"), "rama": fila.get("gitBranch"),
                        "version_claude_code": fila.get("version")}
            nombre_agente = "subagente" if fila.get("isSidechain") and agente == "principal" else agente

            if fila.get("type") == "assistant":
                mensaje = fila.get("message") or {}
                clave = fila.get("requestId") or mensaje.get("id") or fila.get("uuid")
                uso = mensaje.get("usage")
                previa = llamadas.get(clave)
                if uso and (previa is None or uso.get("output_tokens", 0) > previa[2].get("output_tokens", 0)):
                    llamadas[clave] = (modelo_base(mensaje.get("model", "")), nombre_agente, uso, fila.get("effort"))
                for bloque in mensaje.get("content") or []:
                    if not isinstance(bloque, dict) or bloque.get("type") != "tool_use":
                        continue
                    nombre = bloque.get("name", "?")
                    entrada = bloque.get("input") or {}
                    herramientas[nombre] += 1
                    if nombre in HERRAMIENTAS_AGENTE:
                        subagentes[entrada.get("subagent_type") or "general"] += 1
                    if nombre == "Skill":
                        skills[entrada.get("skill", "?")] += 1
                    if nombre in HERRAMIENTAS_EDICION and entrada.get("file_path"):
                        ficheros_editados.add(entrada["file_path"])
                if agente == "principal" and instante:
                    ultimo_asistente = instante

            if fila.get("type") == "user":
                contenido = (fila.get("message") or {}).get("content")
                if isinstance(contenido, list):
                    errores_herramientas += sum(
                        1 for b in contenido if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error")
                    )
                if agente == "principal" and not fila.get("isSidechain") and es_peticion_humana(fila):
                    espera = (instante - ultimo_asistente).total_seconds() if instante and ultimo_asistente else None
                    peticiones.append({"instante": fila.get("timestamp"), "caracteres": len(texto(fila)),
                                       "segundos_desde_ultima_respuesta": espera})

    for modelo, nombre_agente, uso, esfuerzo in llamadas.values():
        sumar_uso(uso_por_modelo[modelo], uso)
        sumar_uso(uso_por_agente[nombre_agente], uso)
        if esfuerzo:
            esfuerzos[esfuerzo] += 1

    instantes.sort()
    inicio, fin = (instantes[0], instantes[-1]) if instantes else (None, None)
    activo = sum(
        min((b - a).total_seconds(), PAUSA_INACTIVA_S) for a, b in zip(instantes, instantes[1:])
    )

    modelos = {}
    coste_total = 0.0
    sin_precio = []
    for modelo, uso in sorted(uso_por_modelo.items()):
        c = coste(uso, precios["modelos"].get(modelo))
        if c is None:
            sin_precio.append(modelo)
        else:
            coste_total += c
        modelos[modelo] = {**uso, "coste_api_usd": round(c, 4) if c is not None else None}

    agentes = {}
    for nombre, uso in sorted(uso_por_agente.items()):
        agentes[nombre] = dict(uso)

    claude_code = None
    if estados_coste:
        # Cada arranque del proceso lleva su propio acumulado: se suma el último de cada arranque.
        claude_code = {
            "coste_usd": round(sum(e.get("totalCostUSD", 0) for e in estados_coste.values()), 4),
            "tiempo_api_s": round(sum(e.get("totalAPIDuration", 0) for e in estados_coste.values()) / 1000),
            "tiempo_herramientas_s": round(sum(e.get("totalToolDuration", 0) for e in estados_coste.values()) / 1000),
            "lineas_anadidas": sum(e.get("totalLinesAdded", 0) for e in estados_coste.values()),
            "lineas_borradas": sum(e.get("totalLinesRemoved", 0) for e in estados_coste.values()),
        }

    esperas = [p["segundos_desde_ultima_respuesta"] for p in peticiones if p["segundos_desde_ultima_respuesta"]]
    total_uso = uso_vacio()
    for uso in uso_por_modelo.values():
        for k in total_uso:
            total_uso[k] += uso[k]
    entrada_total = total_uso["entrada"] + total_uso["lectura_cache"] + total_uso["escritura_cache_5m"] + total_uso["escritura_cache_1h"]

    return {
        **meta,
        "sesiones": sesiones,
        "transcripciones": [str(r) for _, r in fuentes],
        "inicio": inicio.isoformat() if inicio else None,
        "fin": fin.isoformat() if fin else None,
        "duracion_total_min": round((fin - inicio).total_seconds() / 60, 1) if inicio else None,
        "tiempo_activo_min": round(activo / 60, 1),
        "peticiones_humanas": len(peticiones),
        "caracteres_escritos_por_humano": sum(p["caracteres"] for p in peticiones),
        "espera_humana_total_min": round(sum(esperas) / 60, 1),
        "espera_humana_mediana_min": round(sorted(esperas)[len(esperas) // 2] / 60, 1) if esperas else None,
        "llamadas_api": total_uso["llamadas"],
        "llamadas_herramientas": sum(herramientas.values()),
        "errores_herramientas": errores_herramientas,
        "herramientas": dict(herramientas.most_common()),
        "subagentes_lanzados": dict(subagentes.most_common()),
        "skills_usadas": dict(skills.most_common()),
        "ficheros_editados": sorted(ficheros_editados),
        "compactaciones": compactaciones,
        "esfuerzo": dict(esfuerzos),
        "tokens": total_uso,
        "ratio_cache": round(total_uso["lectura_cache"] / entrada_total, 3) if entrada_total else None,
        "por_modelo": modelos,
        "por_agente": agentes,
        "coste_api_usd": round(coste_total, 4),
        "modelos_sin_precio": sin_precio,
        "segun_claude_code": claude_code,
        "peticiones": peticiones,
    }


def numero(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def nombre_agente_telemetria(evento: dict) -> str:
    if evento.get("agent.name"):
        return evento["agent.name"]
    origen = evento.get("query_source") or ""
    if origen in ("sdk", "repl_main_thread", "main") or origen.startswith("repl_main_thread"):
        return "principal"
    return f"auxiliar ({origen or 'desconocido'})"


def analizar_telemetria(carpeta: Path, tarea: str) -> dict | None:
    """Tokens, coste y agentes de la tarea según los eventos del receptor local; None si no hay eventos."""
    eventos = []
    for ruta in sorted(carpeta.glob("*.jsonl")) if carpeta.is_dir() else []:
        eventos += [e for e in leer_jsonl(ruta) if e.get("tarea.id") == tarea]
    llamadas = {}
    for e in eventos:
        if e.get("event.name") == "api_request":
            llamadas[e.get("request_id") or e.get("client_request_id") or id(e)] = e
    if not llamadas:
        return None

    por_modelo: dict[str, dict] = defaultdict(lambda: {**uso_vacio(), "coste_api_usd": 0.0})
    por_agente: dict[str, dict] = defaultdict(lambda: {**uso_vacio(), "coste_api_usd": 0.0})
    esfuerzos: Counter = Counter()
    for e in llamadas.values():
        for destino in (por_modelo[modelo_base(e.get("model", ""))], por_agente[nombre_agente_telemetria(e)]):
            destino["llamadas"] += 1
            destino["entrada"] += int(numero(e.get("input_tokens")))
            destino["salida"] += int(numero(e.get("output_tokens")))
            destino["lectura_cache"] += int(numero(e.get("cache_read_tokens")))
            # La telemetría no separa la caché de 5 min y la de 1 h; cost_usd ya la valora bien.
            destino["escritura_cache_5m"] += int(numero(e.get("cache_creation_tokens")))
            destino["coste_api_usd"] += numero(e.get("cost_usd"))
        if e.get("effort"):
            esfuerzos[e["effort"]] += 1
    for grupo in (por_modelo, por_agente):
        for uso in grupo.values():
            uso["coste_api_usd"] = round(uso["coste_api_usd"], 4)

    resultados = [e for e in eventos if e.get("event.name") == "tool_result"]
    instancias = Counter(e.get("agent_type", "?") for e in eventos if e.get("event.name") == "subagent_completed")
    total = uso_vacio()
    for uso in por_modelo.values():
        for k in total:
            total[k] += uso[k]
    entrada_total = total["entrada"] + total["lectura_cache"] + total["escritura_cache_5m"]
    return {
        "fuente_tokens": "telemetria",
        "sesiones_telemetria": sorted({e["session.id"] for e in eventos if e.get("session.id")}),
        "llamadas_api": total["llamadas"],
        "tokens": total,
        "ratio_cache": round(total["lectura_cache"] / entrada_total, 3) if entrada_total else None,
        "por_modelo": dict(sorted(por_modelo.items())),
        "por_agente": dict(sorted(por_agente.items())),
        "coste_api_usd": round(sum(numero(e.get("cost_usd")) for e in llamadas.values()), 4),
        "modelos_sin_precio": [],
        "esfuerzo": dict(esfuerzos),
        "errores_herramientas": sum(1 for e in resultados if str(e.get("success")).lower() == "false"),
        "subagentes_terminados": dict(instancias.most_common()),
    }


def markdown(m: dict, slug: str) -> str:
    def n(x):
        return f"{x:,}".replace(",", ".") if isinstance(x, int) else str(x)

    filas_modelo = "\n".join(
        f"| {mod} | {n(u['llamadas'])} | {n(u['entrada'])} | {n(u['salida'])} | {n(u['razonamiento'])} | "
        f"{n(u['lectura_cache'])} | {n(u['escritura_cache_5m'] + u['escritura_cache_1h'])} | {u['coste_api_usd']} |"
        for mod, u in m["por_modelo"].items()
    )
    filas_agente = "\n".join(
        f"| {ag} | {n(u['llamadas'])} | {n(u['salida'])} | {n(u['lectura_cache'])} | {u.get('coste_api_usd', '-')} |"
        for ag, u in m["por_agente"].items()
    )
    cc = m["segun_claude_code"]
    de_telemetria = m.get("fuente_tokens") == "telemetria"
    fuente = (
        "- Tokens y coste de la telemetría de Claude Code (salida real de cada llamada, subagentes incluidos); la "
        "escritura de caché va sin separar 5 min y 1 h."
        if de_telemetria else
        "- Tokens de las transcripciones: la salida de cada mensaje es la que había al empezar la respuesta, así que "
        "se queda corta. Lanza la sesión con `lanzar.sh` para tener la cifra exacta."
    )
    linea_cc = (
        f"- Último resumen que guardó Claude Code (puede ir por detrás de los últimos mensajes): {cc['coste_usd']} USD, {cc['tiempo_api_s']} s de API, "
        f"{cc['tiempo_herramientas_s']} s de herramientas, +{cc['lineas_anadidas']} / -{cc['lineas_borradas']} líneas."
        if cc else "- Claude Code no dejó resumen de coste en esta transcripción."
    )
    aviso = f"\n- Modelos sin precio en la tabla: {', '.join(m['modelos_sin_precio'])}." if m["modelos_sin_precio"] else ""
    return f"""# Métricas de la sesión: {slug}

- Sesiones: {', '.join(f'`{s}`' for s in m['sesiones'])} en `{m.get('cwd')}` (rama `{m.get('rama')}`, Claude Code {m.get('version_claude_code')})
- Inicio y fin: {m['inicio']} → {m['fin']}
- Duración total: {m['duracion_total_min']} min. Tiempo activo (sin pausas de más de 5 min): {m['tiempo_activo_min']} min.

## Personas

- Peticiones humanas: {m['peticiones_humanas']} ({n(m['caracteres_escritos_por_humano'])} caracteres).
- Espera hasta cada respuesta humana: {m['espera_humana_total_min']} min en total, mediana {m['espera_humana_mediana_min']} min.
  Es una cota superior del tiempo que ha dedicado la persona: incluye el tiempo en que estaba haciendo otra cosa.

## Trabajo

- Llamadas a la API: {n(m['llamadas_api'])}. Llamadas a herramientas: {n(m['llamadas_herramientas'])} ({m['errores_herramientas']} con error).
- Subagentes lanzados: {json.dumps(m['subagentes_lanzados'], ensure_ascii=False)}
- Skills: {json.dumps(m['skills_usadas'], ensure_ascii=False)}
- Herramientas: {json.dumps(m['herramientas'], ensure_ascii=False)}
- Ficheros editados: {len(m['ficheros_editados'])}. Compactaciones del contexto: {m['compactaciones']}.
- Esfuerzo: {json.dumps(m['esfuerzo'], ensure_ascii=False)}

## Tokens y coste a precio de API

| Modelo | Llamadas | Entrada | Salida | De ella, razonamiento | Lectura de caché | Escritura de caché | USD |
|---|---|---|---|---|---|---|---|
{filas_modelo}

- **Coste total a precio de API: {m['coste_api_usd']} USD.** Ratio de caché: {m['ratio_cache']} de la entrada se leyó de caché.
{fuente}
{linea_cc}{aviso}

| Agente | Llamadas | Salida | Lectura de caché | USD |
|---|---|---|---|---|
{filas_agente}
"""


def main() -> None:
    args = leer_args()
    principales = localizar_sesiones(args)
    precios = json.loads(Path(args.precios).read_text(encoding="utf-8"))
    m = analizar(principales, precios)
    telemetria = analizar_telemetria(Path(args.telemetria).expanduser(), args.slug)
    if telemetria:
        m.update(telemetria)
    else:
        m["fuente_tokens"] = "transcripciones"
    m["generado"] = datetime.now(timezone.utc).isoformat()

    salida = Path(args.salida).expanduser() if args.salida else Path(args.repo).expanduser().resolve() / ".agentes" / "metricas"
    salida.mkdir(parents=True, exist_ok=True)
    base = f"{datetime.now().strftime('%Y-%m-%d')}-{args.slug}"
    (salida / f"{base}.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    (salida / f"{base}.md").write_text(markdown(m, args.slug), encoding="utf-8")
    print(salida / f"{base}.md")
    print(salida / f"{base}.json")


if __name__ == "__main__":
    main()
