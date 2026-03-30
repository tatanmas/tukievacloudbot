# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Cron (`crontab.tuki`, pipeline-monitor)

- **`crontab crontab.tuki` en el Mac no funciona** con las rutas `/workspace/...`: ese prefijo es **solo dentro del contenedor** Docker. En macOS no existe `/workspace`.
- Para automatizar desde el Mac: **`docker exec clawd-clean-gateway bash -lc 'cd /workspace/skills/pipeline-monitor && ./morning_report.sh'`** (probar a mano) y luego crontab con `docker exec` como en **`crontab.mac.example`**. Detalle: **`docs/CRON-TUKI.md`**.

## Chrome / Control UI / extensión (gateway en Docker)

- **`clawdbot devices pending` no existe.** Usar: `clawdbot devices list` (muestra pendientes y emparejados).
- Si el CLI en el Mac responde **`pairing required`** al hablar con `ws://127.0.0.1:18789`, el estado vive en el volumen Docker: ejecutar **dentro del contenedor**:
  - `docker exec clawd-clean-gateway clawdbot devices list`
  - `docker exec clawd-clean-gateway clawdbot devices approve <requestId>`
- **`device signature expired` en logs:** suele haber un **request pendiente** o token viejo; tras aprobar o re‑conectar la extensión, el error debería cesar.
- **Extensión Chrome / relay:** en Clawdbot hay **dos** puertos distintos:
  - **`18791`** → servidor **Express** de control del navegador (respuesta JSON con `enabled`, `cdpUrl`, etc.). **No** es el relay que espera la extensión para el check “Save”.
  - **`18792`** → **relay de la extensión** (`extension-relay`): `GET /` devuelve texto **`OK`**. En la extensión OpenClaw pon **Port `18792`**. URL efectiva: `http://127.0.0.1:18792/`.
- **Docker Desktop (Mac):** si el relay escucha solo en **`127.0.0.1`** dentro del contenedor, el reenvío de puertos del host **no llega** al proceso (el tráfico entra por la interfaz `172.x`, no por loopback). Síntoma: `curl` desde el Mac → **`Empty reply from server`**, pero `docker exec … curl http://127.0.0.1:18792` → **`OK`**. En **`.clawdbot/clawdbot.json`** el perfil `browser.profiles.chrome.cdpUrl` debe ser **`http://0.0.0.0:18792`** para que el relay escuche en todas las interfaces y el mapeo `127.0.0.1:18792->18792` funcione.
- El log **`Browser control listening on http://127.0.0.1:18791/`** se refiere al servidor Express; el relay sigue en **18792**.
- El `docker-compose` del repo usa **`18792:18792`** (no mezclar con 18791).
- **Badge rojo (!) pero en Options dice “Relay reachable”:** suele ser **estado viejo** del service worker o que el badge mide **WebSocket/pestaña adjunta**, no el mismo chequeo que la página. Hacer **“Volver a cargar”** en el banner de la página de opciones, luego **chrome://extensions → Recargar** la extensión, y probar el icono en una **pestaña web normal** (adjuntar). Si el relay responde `OK` con `curl` y Options está en verde, el relay **está bien** aunque el ! tarde en quitarse.
- **Icono siempre rojo al clic (Maps, etc.) con gateway en Docker:** el relay aceptaba **HTTP** desde el Mac pero rechazaba el **WebSocket** (`upgrade`) porque la IP de origen dentro del contenedor es **172.x** (NAT de Docker), no `127.0.0.1`. La imagen aplica **`patches/patch-extension-relay-docker.js`** para permitir esas IPs. Tras actualizar el repo: **`docker compose build clawdbot-gateway && docker compose up -d --force-recreate clawdbot-gateway`**, luego recargar la extensión y volver a adjuntar la pestaña.
- **Salida OK de `devices list`:** tabla **Paired (N)** sin sección **Pending** (o Pending vacío). El warning de **`punycode`** en stderr es cosmético. Más contexto en **`docs/LOGS.md`** (verificación rápida + líneas `device signature expired`).

## Tuki — API de integración (operativo, solo lectura)

- **`TUKI_INTEGRATION_TOKEN`** en **`.env`**. Tras cambiarlo: **`docker compose up -d --force-recreate`** para que exec/sandbox lo reciba (igual que Notion). Si ya tienes **`TUKI_API_BASE_URL`** (p. ej. `https://api.tuki.cl/api/v1/`), el script `tuki_api.sh` la usa como base salvo que definas **`TUKI_INTEGRATION_BASE_URL`**.
- **No** uses `web_fetch` a `tuki.cl` con Bearer: el token no suele estar en ese contexto. **Correcto:** **exec** con el script del skill:
  - `bash /workspace/skills/tuki-integration-api/scripts/tuki_api.sh capabilities`
  - luego `snapshot` u `orders-summary` según `skills/tuki-integration-api/SKILL.md`.
- Flujo: **siempre** `capabilities` primero; scopes `snapshot` y `orders` según el token. **403** en `orders-summary` → falta scope `orders` (SuperAdmin → API integración LLM).
- **Growth:** ritmo y reglas en **`docs/GROWTH-EVA.md`** (pulso Tuki + Notion + preguntar a Tatan lo que la API no cubre).
- **Red agentes / sync / carga:** arquitectura por fases en **`docs/RED-AGENTES-TUKI-NOTION.md`**; prompt listo para Cursor en **`docs/CURSOR-PROMPT-EVA-SYNC-CARGA.md`**; checklist de campos (completar desde backend) en **`docs/CHECKLIST-CARGA-TUKI.md`**.
- **Pulso growth automático:** `skills/tuki-integration-api/scripts/growth_pulse.sh` escribe `data/pulses/latest-growth-pulse.md` (cron vía `docker exec`, ver **`docs/PULSO-GROWTH-CRON.md`** y `crontab.mac.example`).
- **Pulso secuencial:** `bash /workspace/skills/tuki-integration-api/scripts/tuki_pulse.sh` (opcional `--json-out DIR`). Sync Notion ↔ IDs Tuki: skill **`skills/tuki-notion-sync/`**, exports en **`data/sync/`**, script `sync_leads_from_export.py`.

## Notion (no olvidar)

- **NOTION_TOKEN** y, si aplica, **NOTION_NOTES_DB_ID** y **NOTION_ACTIONABLES_DB_ID** están en **`.env`** (raíz del repo).
- El gateway carga `.env` vía `env_file` y ahora pasa estas variables explícitamente en `environment` para que el proceso que ejecuta comandos (exec/sandbox) las reciba.
- **Si algo dice "No hay API key de Notion configurada":** la key sí está en `.env`. Hace falta **reiniciar el gateway** para que tome las variables: `docker compose up -d --force-recreate`.
- **`web_fetch` y Notion (401 "API token is invalid"):** la herramienta **web_fetch** del gateway **no** usa `NOTION_TOKEN` del `.env`. Si el modelo llama a `https://api.notion.com/...` vía web_fetch, Notion responde **401** salvo que el propio modelo ponga un Bearer válido (mala práctica). **Correcto:** usar **exec** (o scripts del skill, p. ej. `skills/tuki-leads-db/scripts/*.py`) donde el proceso hereda `NOTION_TOKEN` del contenedor, o `curl` con `-H "Authorization: Bearer $NOTION_TOKEN"` y `-H "Notion-Version: 2022-06-28"`.
- **`read tool called without path`:** el modelo emitió una llamada `read` mal formada (sin `path`); suele ser ruido del modelo; reintentar o pedir explícitamente leer `ruta/archivo`.
- **Skills y “brew not installed”:** el dashboard asume Mac + Homebrew; el gateway Docker es **Linux**. **`goplaces`** y **`gog`** ya se instalan en la **imagen** (ver **`Dockerfile`**). Places necesita **`GOOGLE_PLACES_API_KEY`** en `.env` y recrear el contenedor. Detalle: **`docs/SKILLS-DOCKER.md`**.

## API / créditos (Claude, Kimi)

- **Anthropic (Claude):** Org "Tuki" tiene límite de $5/mes; al superarlo pausan hasta el 1 del mes siguiente (medianoche UTC). Ver **CREDITS-API.md** para el registro de cuándo se agotan créditos o se pausa.
- **Fallback:** Si Claude falla o se acaban los créditos, el gateway usa **Kimi** (nvidia/moonshotai/kimi-k2.5). Es **hexagonal** (decisión en el gateway, no en instrucciones de la LLM). Config en `.clawdbot/clawdbot.json` → `agents.defaults.model.primary` + `fallbacks`. Detalle: **docs/FALLBACK-MODELO.md**. Si el chat no pasa a Kimi, revisar CREDITS-API.md y logs; a veces "usage limits" no dispara fallback (bug conocido).

## Chat: mensajes largos o sin respuesta

- Si envías un **mensaje muy largo** o el **historial ya es largo** y el agente no responde (solo queda el timestamp sin burbuja): el run puede completar en ~1 s por límite de contexto y no generar respuesta visible.
- **Qué hacer:** (1) Usar **Nueva sesión** y pegar el mensaje ahí (contexto fresco). (2) O resumir el mensaje en menos líneas.

### “Escribiendo…” largo, recargo y no veo nada

- Con **Kimi + muchas tools** un run puede tardar **1–3+ minutos**. La UI muestra “trabajando” pero **no siempre deja claro** si va por el minuto 0:30 o el 2:00.
- **`chat.send` en ~50 ms** solo confirma que el mensaje entró; **no** significa que el modelo ya respondió.
- En el log interno del contenedor aparece al cerrar: `embedded run done … durationMs=… aborted=false`. Ejemplo real: **~107 s** entre envío y fin de run.
- Si **recargas antes** de que termine el run, puedes **perder la burbuja en vivo**; a veces al volver la transcripción **sí** está, a veces **no** (nueva conexión WebSocket / misma sesión / bug de UI).
- **Señal de que sigue trabajando:** otra terminal con `docker compose logs -f clawdbot-gateway` y/o `docker exec clawd-clean-gateway tail -f /tmp/clawdbot/clawdbot-$(date -u +%Y-%m-%d).log` hasta ver `embedded run done` para ese turno.
- **Regla práctica:** con mensajes pesados, esperar **al menos ~2 min** antes de F5; si no hay `embedded run done` en log, entonces sí sospechar cuelgue.

## Autonomía (subagentes)

Para que “hagan solos” sin tropezar con Docker, Notion, Places y timeouts: leer **`AGENTS.md` → sección "Autonomía (subagentes, Docker, misiones largas)"**. Resumen: **Notion → exec/scripts**; **geo → `goplaces` + `GOOGLE_PLACES_API_KEY`**; **browser → pestaña adjunta en Chrome**; **misiones acotadas** y **pivotar** tras 2 fallos iguales.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
