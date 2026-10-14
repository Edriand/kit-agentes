#!/usr/bin/env bash
# Abre Claude Code con el kit y la telemetría de la tarea encendida.
#
# Uso:
#   lanzar.sh <tarea> [opciones de claude]
#   lanzar.sh research-debate --model sonnet
#
# Arranca, si no está ya, el receptor local de telemetría (solo escucha en 127.0.0.1) y abre Claude Code con cada
# evento etiquetado con la tarea, el repo y la versión del kit. Después, metricas_sesion.py saca de ahí la cifra
# exacta de tokens y coste por modelo y por agente, sin salir con /exit y sin pasarle el nombre de la tarea.
#
# Variables opcionales: KIT_DIR (por defecto, la carpeta de este script), KIT_TELEMETRIA (~/.kit-agentes/telemetria),
# KIT_PUERTO_TELEMETRIA (4318).
set -euo pipefail

if [ $# -lt 1 ] || [ "${1#-}" != "$1" ]; then
  echo "Uso: $(basename "$0") <tarea> [opciones de claude]" >&2
  exit 2
fi
tarea="$1"
shift
# El nombre va en OTEL_RESOURCE_ATTRIBUTES, que no admite espacios ni comas.
if ! printf '%s' "$tarea" | grep -Eq '^[a-z0-9][a-z0-9-]{0,62}$'; then
  echo "El nombre de la tarea solo puede tener minúsculas, números y guiones (por ejemplo, research-debate)." >&2
  exit 2
fi

dir_script="$(cd "$(dirname "$0")" && pwd)"
kit_dir="${KIT_DIR:-$dir_script}"
carpeta="${KIT_TELEMETRIA:-$HOME/.kit-agentes/telemetria}"
puerto="${KIT_PUERTO_TELEMETRIA:-4318}"
receptor="$kit_dir/skills/orquestar/scripts/receptor_telemetria.py"

if [ ! -f "$kit_dir/.claude-plugin/plugin.json" ]; then
  echo "No encuentro el kit en $kit_dir. Indica dónde está con KIT_DIR." >&2
  exit 1
fi
version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("version", "desconocida"))' \
  "$kit_dir/.claude-plugin/plugin.json")"
repo="$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" | tr -c 'A-Za-z0-9._\n-' '_')"

# Solo vale nuestro receptor: otro colector en el mismo puerto (por ejemplo, un agente de Datadog con OTLP)
# recibiría los comandos y parámetros de las herramientas y podría sacarlos del equipo.
receptor_vivo() {
  python3 - "$puerto" <<'PY'
import json, sys, urllib.request
abrir = urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    with abrir.open(f"http://127.0.0.1:{sys.argv[1]}/salud", timeout=0.5) as r:
        sys.exit(0 if json.load(r).get("servicio") == "kit-agentes-telemetria" else 1)
except Exception:
    sys.exit(1)
PY
}

puerto_ocupado() {
  python3 - "$puerto" <<'PY'
import socket, sys
s = socket.socket()
s.settimeout(0.5)
sys.exit(0 if s.connect_ex(("127.0.0.1", int(sys.argv[1]))) == 0 else 1)
PY
}

telemetria=1
if ! receptor_vivo; then
  if puerto_ocupado; then
    echo "Aviso: el puerto $puerto lo usa otro servicio. Sigo sin telemetría (cambia de puerto con KIT_PUERTO_TELEMETRIA)." >&2
    telemetria=0
  else
    mkdir -p "$carpeta"
    chmod 700 "$carpeta"
    nohup python3 "$receptor" --puerto "$puerto" --carpeta "$carpeta" >>"$carpeta/receptor.log" 2>&1 &
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      receptor_vivo && break
      sleep 0.3
    done
    if ! receptor_vivo; then
      echo "Aviso: el receptor de telemetría no arrancó (mira $carpeta/receptor.log). Sigo sin telemetría." >&2
      telemetria=0
    fi
  fi
fi

export KIT_TAREA="$tarea"
if [ "$telemetria" = 1 ]; then
  export KIT_TELEMETRIA="$carpeta"
  export CLAUDE_CODE_ENABLE_TELEMETRY=1
  export OTEL_METRICS_EXPORTER=none
  export OTEL_LOGS_EXPORTER=otlp
  export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=http/json
  export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT="http://127.0.0.1:$puerto/v1/logs"
  # Sin esto, los agentes del kit salen como "custom". El receptor borra los parámetros y comandos que también manda.
  export OTEL_LOG_TOOL_DETAILS=1
  export OTEL_RESOURCE_ATTRIBUTES="tarea.id=$tarea,cliente.repo=$repo,kit.version=$version"
fi

exec claude --plugin-dir "$kit_dir" "$@"
