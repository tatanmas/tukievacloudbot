--- 
name: tuki-integration-api
description: Consultar datos operativos de la plataforma Tuki vía API de integración (solo lectura). Usar para inventario, salud, destinos, guías, actividad del día, resumen de órdenes e ingresos alineados con Tuki.
---

# Tuki — API de integración (solo lectura)

Eres un asistente que consulta datos operativos de la plataforma **Tuki** mediante su API de integración. **Solo métodos GET**; no crees ni modifiques datos por esta API.

## Autenticación

- Usa el token en la variable de entorno **`TUKI_INTEGRATION_TOKEN`** (o la que configure el administrador en el despliegue).
- En cada petición HTTP incluye exactamente:
  - `Authorization: Bearer <token>`
- **No** pidas al usuario contraseñas, JWT de SuperAdmin ni credenciales. Si falta el token, indica que quien despliega el servicio debe configurarlo en `.env` y **recrear el gateway** (`docker compose up -d --force-recreate`).

## Base URL

- Si defines **`TUKI_INTEGRATION_BASE_URL`**, úsala como prefijo.
- Si no, y en `.env` tienes **`TUKI_API_BASE_URL`** (p. ej. `https://api.tuki.cl/api/v1/`), el script **`tuki_api.sh`** usa esa misma base para no duplicar host.
- Si ninguna: default `https://tuki.cl/api/v1`.

**Backend:** las vistas de integración **no** usan `JWTAuthentication` sobre el `Bearer` (evita confundir `tuki_...` con un access JWT). La validez del token la resuelve el permiso de integración (`HasIntegrationToken` o equivalente).

## Flujo obligatorio

1. **Siempre primero** (para endpoints actualizados, `agent_rules_es`, `documentation_markdown`):
   - `GET /integrations/v1/capabilities/`
2. Según la pregunta:
   - Inventario, salud de plataforma, destinos, guías, actividad aproximada del día →  
     `GET /integrations/v1/snapshot/`  
     (requiere scope **`snapshot`** en el token)
   - Órdenes, estados de pago, revenue agregado alineado con Tuki →  
     `GET /integrations/v1/orders/summary/`  
     (requiere scope **`orders`** en el token)

## Ejecución en este workspace (gateway Docker)

Desde **exec** en el contenedor (hereda `.env`):

```bash
bash /workspace/skills/tuki-integration-api/scripts/tuki_api.sh capabilities
bash /workspace/skills/tuki-integration-api/scripts/tuki_api.sh snapshot
bash /workspace/skills/tuki-integration-api/scripts/tuki_api.sh orders-summary
```

### Pulso en secuencia (chat / una sola corrida)

```bash
bash /workspace/skills/tuki-integration-api/scripts/tuki_pulse.sh
# Opcional: guardar JSON en disco
bash /workspace/skills/tuki-integration-api/scripts/tuki_pulse.sh --json-out /workspace/data/pulse/$(date +%Y-%m-%d)
```

### Pulso programado (cron, “equipo growth” sin LLM)

Solo **snapshot + orders** → Markdown + JSON en `data/pulses/` (ver **`docs/PULSO-GROWTH-CRON.md`**):

```bash
bash /workspace/skills/tuki-integration-api/scripts/growth_pulse.sh
```

Genera `latest-growth-pulse.md` y `snapshot-latest.json` / `orders-latest.json`. Eva puede **leer ese Markdown** cuando pidas resumen sin repetir llamadas a la API.

Si `orders-summary` falla (**403**), revisar scope `orders` en el token. `tuki_pulse` sigue aunque falle orders si está diseñado así.

### Listados por tipo (alojamiento, experiencia, …)

**No implementado** en la API de integración actual. Stub informativo:

```bash
bash /workspace/skills/tuki-integration-api/scripts/tuki_resource_lists_stub.sh accommodations
```

Sale con código **5** hasta que existan GET documentados en el backend. No inventar URLs.

El script escribe el código HTTP en stderr. Si `orders-summary` devuelve **403**, el token no incluye scope `orders`: dilo claro y sugiere crear otro token con ese scope en **SuperAdmin → API integración LLM**.

## Interpretación (no inventar)

- **`activity_today`**: no es DAU perfecto; son proxies (registros del día, logins, etc.). No afirmes métricas que no vengan en el JSON.
- **`revenue_eligible`**: sigue las reglas oficiales de Tuki; no inventes cifras.

## Límites

- Solo **GET**. Si recibes 403 en `orders/summary`, explica el tema de scopes (arriba).
