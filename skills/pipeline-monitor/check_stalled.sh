#!/bin/bash
# Check Stalled Leads - Detecta leads sin movimiento
# Ejecutar cada día a las 9am

DATABASE_ID="${NOTION_LEADS_DB_ID:-303ddd5f-c230-8087-9f4b-f6f51c7f5ded}"

echo "🚨 LEADS ESTANCADOS - Revisión $(date +%Y-%m-%d)"
echo "================================================"

if [ -z "$NOTION_TOKEN" ]; then
  echo "ERROR: NOTION_TOKEN no está definido."
  exit 1
fi

# Nota: no usar `curl | python3 <<EOF`: el heredoc consume stdin y json.load recibe vacío.
curl -sS -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "and": [
        {"property": "Estado", "status": {"does_not_equal": "Publicado y operativo"}},
        {"property": "Estado", "status": {"does_not_equal": "Perdido"}}
      ]
    },
    "sorts": [{"timestamp": "created_time", "direction": "descending"}]
  }' | python3 -c "$(cat <<'PYTHON'
import json
import sys
from datetime import datetime

raw = sys.stdin.read()
if not raw.strip():
    print("ERROR: respuesta vacía de la API de Notion (¿red o token?).")
    sys.exit(1)
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print("ERROR: la API no devolvió JSON válido:", e)
    print(raw[:500])
    sys.exit(1)
if data.get("object") == "error":
    print("ERROR Notion:", data.get("code"), data.get("message"))
    sys.exit(1)

leads = data.get("results", [])

hoy = datetime.now()
alerts = {
    "critica": [],
    "media": [],
    "seguimiento": [],
}

for lead in leads:
    props = lead.get("properties", {})
    nombre = props.get("Nombre del Leapd", {}).get("title", [{}])[0].get("text", {}).get("content", "Sin nombre")
    estado = props.get("Estado", {}).get("status", {}).get("name", "Desconocido")
    creado = lead.get("created_time", "")
    ultima_ed = lead.get("last_edited_time", creado)

    try:
        fecha_edicion = datetime.fromisoformat(ultima_ed.replace("Z", "+00:00"))
        dias_sin_mov = (hoy - fecha_edicion.replace(tzinfo=None)).days
    except Exception:
        dias_sin_mov = 0

    if estado == "Contactar" and dias_sin_mov >= 5:
        alerts["critica"].append({"nombre": nombre, "dias": dias_sin_mov, "estado": estado})
    elif estado == "Esperando información" and dias_sin_mov >= 3:
        alerts["media"].append({"nombre": nombre, "dias": dias_sin_mov, "estado": estado})
    elif estado == "Esperando respuesta" and dias_sin_mov >= 7:
        alerts["seguimiento"].append({"nombre": nombre, "dias": dias_sin_mov, "estado": estado})

print("\n🔴 ALERTAS CRÍTICAS (Contactar >5 días):")
for item in alerts["critica"]:
    print(f"   • {item['nombre'][:40]}... ({item['dias']} días)")

print("\n🟡 ALERTAS MEDIA (Esperando info >3 días):")
for item in alerts["media"]:
    print(f"   • {item['nombre'][:40]}... ({item['dias']} días)")

print("\n🟠 ALERTAS SEGUIMIENTO (Esperando respuesta >7 días):")
for item in alerts["seguimiento"]:
    print(f"   • {item['nombre'][:40]}... ({item['dias']} días)")

total_alerts = len(alerts["critica"]) + len(alerts["media"]) + len(alerts["seguimiento"])
print(f"\n📊 Total alertas: {total_alerts}")
PYTHON
)"
