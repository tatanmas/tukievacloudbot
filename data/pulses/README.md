# data/pulses

Salidas del script **`skills/tuki-integration-api/scripts/growth_pulse.sh`** (pulso programado de snapshot + órdenes).

- **`latest-growth-pulse.md`** — resumen legible (última corrida).
- **`snapshot-latest.json`**, **`orders-latest.json`** — última respuesta cruda de la API.
- **`snapshot-*.json`**, **`orders-*.json`** — histórico por timestamp UTC (pueden crecer; rotar o ignorar en git).

Los `*.json` suelen estar en **`.gitignore`** para no inflar el repo.
