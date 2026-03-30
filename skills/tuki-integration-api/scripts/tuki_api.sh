#!/usr/bin/env bash
# Tuki Integration API (solo GET). Requiere TUKI_INTEGRATION_TOKEN en el entorno.
set -euo pipefail

# Base: explícita > mismo host que TUKI_API_BASE_URL (tu .env) > tuki.cl
BASE="${TUKI_INTEGRATION_BASE_URL:-}"
if [[ -z "$BASE" && -n "${TUKI_API_BASE_URL:-}" ]]; then
  BASE="${TUKI_API_BASE_URL%/}"
fi
if [[ -z "$BASE" ]]; then
  BASE="https://tuki.cl/api/v1"
fi
TOKEN="${TUKI_INTEGRATION_TOKEN:-}"

usage() {
  cat <<'EOF'
Uso: tuki_api.sh <comando>

Comandos:
  capabilities   GET /integrations/v1/capabilities/  (siempre primero en un flujo nuevo)
  snapshot       GET /integrations/v1/snapshot/     (scope "snapshot")
  orders-summary GET /integrations/v1/orders/summary/ (scope "orders")

Variables:
  TUKI_INTEGRATION_TOKEN  Bearer token (obligatorio)
  TUKI_INTEGRATION_BASE_URL  prefijo API (opcional)
  TUKI_API_BASE_URL  si no defines INTEGRATION_BASE_URL, se usa este (p. ej. https://api.tuki.cl/api/v1)
  (default final: https://tuki.cl/api/v1)

Salida: cuerpo JSON (pretty con jq si está instalado) y código HTTP en stderr.
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

if [[ -z "$TOKEN" ]]; then
  echo "tuki_api.sh: falta TUKI_INTEGRATION_TOKEN. Quien despliega el servicio debe definirla en .env y recrear el gateway." >&2
  exit 2
fi

cmd="$1"
path=""
case "$cmd" in
  capabilities) path="/integrations/v1/capabilities/" ;;
  snapshot) path="/integrations/v1/snapshot/" ;;
  orders-summary) path="/integrations/v1/orders/summary/" ;;
  -h|--help|help) usage; exit 0 ;;
  *) echo "Comando desconocido: $cmd" >&2; usage; exit 1 ;;
esac

url="${BASE%/}${path}"
tmp="$(mktemp)"
code_file="$(mktemp)"
cleanup() { rm -f "$tmp" "$code_file"; }
trap cleanup EXIT

http_code=$(curl -sS -o "$tmp" -w "%{http_code}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" \
  "$url") || true

echo "$http_code" >"$code_file"

if command -v jq >/dev/null 2>&1; then
  jq '.' <"$tmp" 2>/dev/null || cat "$tmp"
else
  cat "$tmp"
fi

echo "HTTP $http_code" >&2

if [[ "$http_code" == "403" && "$cmd" == "orders-summary" ]]; then
  echo "tuki_api.sh: 403 en orders/summary — el token probablemente no tiene scope \"orders\". En SuperAdmin → API integración LLM, crear un token con ese scope." >&2
fi

if [[ "$http_code" =~ ^[45] ]]; then
  exit 3
fi
