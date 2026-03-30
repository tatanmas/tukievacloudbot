# Lista de cosas prohibidas de migrar a clawd-clean

Todo lo siguiente pertenece al repo viejo (clawd) y **no** debe copiarse ni reutilizarse en clawd-clean.

## Estado y config

- **`.clawdbot/`** — Config, sesiones, cron, devices, credentials, identity, logs. Estado contaminado y atado al setup anterior.

## UI y flujos custom

- **`canvas/`** (raíz del repo viejo)
- **`clawd/canvas/`** — HTML, chat-comfy, etc. Base limpia usa solo la UI stock del gateway.

## Cron y automatización

- **`cron-jobs-tuki.json`**
- **`.clawdbot/cron/`** — Jobs registrados. Sin cron en la base mínima.

## Docker y runtime viejos

- **`entrypoint.sh`** — Limpieza de locks y cron-sync. Base stock no lo usa.
- **`docker-compose.yml`** del repo viejo — Speaches, docker-socket-proxy, volúmenes de sesiones, paths Mac.
- **`Dockerfile`** del repo viejo — Patch sandbox-paths, entrypoint custom.
- **`Dockerfile.sandbox`** — Opcional en fases posteriores; no en base mínima.
- **`patches/sandbox-paths.js`** — Workaround; no en base limpia.

## Volúmenes y sesiones

- **Volumen `clawdbot-sessions`** y cualquier montaje sobre `.clawdbot/agents/main/sessions` del setup viejo.
- Cualquier **estado persistente roto** (locks, sesiones corruptas, logs del gateway anterior).

## Secretos

- **`.env.docker`**, **`.env.tuki`** y cualquier archivo con tokens o API keys del repo viejo. Cargar valores nuevos en `.env` de clawd-clean y rotar si hubo exposición.

## Otros (referencia)

- Backups del repo viejo (`backups/`, `backup_*.json`).
- Scripts que invocan `clawdbot` en el host o cron (`claw-host.sh`, `cron-register.sh`, etc.) hasta que en Fase 2 se reintroduzca cron de forma controlada.
- Documentación de auditorías/workarounds (AUDIT-*, BUG-*, WORKAROUND-*, RESTAURACION-*, etc.); útil solo como referencia en el repo viejo, no migrar a clawd-clean.

---

En clawd-clean solo se migra el **contexto controlado** listado en PLAN-CLAWD-CLEAN.md (SOUL, USER, MEMORY, HEARTBEAT, AGENTS) y opcionalmente `memory/*.md` reciente.
