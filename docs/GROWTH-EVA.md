# Growth — Eva (Tuki)

Guía operativa: **datos de la plataforma + preguntas a Tatan** cuando falte contexto de negocio.

## Fuentes de verdad

1. **API de integración Tuki** (solo GET, token en `TUKI_INTEGRATION_TOKEN`): skill `skills/tuki-integration-api/`, script `scripts/tuki_api.sh` desde `exec` en el gateway.
2. **Notion** — backlog, metas semanales, tareas (contexto Eva / Eva Backlog).
3. **`MEMORY.md` / `memory/YYYY-MM-DD.md`** — lo que Tatan ya definió como prioridad.

## Ritmo sugerido

| Cuándo | Qué hacer |
|--------|-----------|
| Pulso o review (chat) | `capabilities` → `snapshot` y `orders-summary` (o `tuki_pulse.sh`). |
| Pulso automático (sin gastar chat) | `growth_pulse.sh` por **cron** → `data/pulses/latest-growth-pulse.md`. Detalle: **`docs/PULSO-GROWTH-CRON.md`**. |
| Si falta meta | Preguntar objetivo concreto (ingresos, reservas, destino a empujar) y crear tarea o nota en Notion. |
| Heartbeat | Rotar ítems en `HEARTBEAT.md` (Tuki + brecha de growth). |

## Reglas

- No afirmar métricas que no estén en el JSON de la API.
- `activity_today` no es DAU perfecto; dilo si alguien interpreta mal.
- No exponer tokens ni pegar secretos en chats públicos.
