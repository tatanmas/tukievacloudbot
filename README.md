# clawd-clean

Entorno nuevo, limpio y paralelo para Clawdbot: asistente personal serio, seguro y dockerizado en Mac.

- **Base:** Clawdbot stock (sin patches ni canvas custom).
- **Un agente:** `main`. Claude primary, Kimi fallback.
- **UI:** Webchat stock del gateway (`/chat`).
- **Sin al inicio:** cron, WhatsApp, sesiones heredadas.

## Arranque rápido

1. `cp .env.example .env` y editar con tu token y API keys.
2. `docker compose build`
3. `docker compose run --rm clawdbot-gateway clawdbot onboard` (primera vez; genera config en `.clawdbot/`).
4. Ajustar si hace falta workspace en `.clawdbot/clawdbot.json` (debe ser `/workspace`).
5. `docker compose up -d`
6. Abrir `http://127.0.0.1:18789` → Settings para pegar token; luego `/chat?session=agent:main:main&token=TU_TOKEN`.

Documentación del proyecto en **docs/**: `docs/ARRANQUE.md`, `docs/VALIDACION.md`, `docs/SECRETS.md`, `docs/SLACK.md` (conectar Clawdbot a Slack), `docs/FASE-2-CRECIMIENTO.md`, `docs/CREDITS-API.md`, `docs/FALLBACK-MODELO.md` (fallback hexagonal gateway), `docs/LOGS.md`, etc.

## Repositorio en GitHub

Este workspace está pensado para versionar **skills**, `AGENTS.md`, `docker-compose`, parches y documentación, sin secretos (`.env` va en `.gitignore`; solo se commitea `.env.example`).

### Crear el repo remoto y subir

1. En GitHub: **New repository** → nombre (p. ej. `clawd-clean`) → **sin** README/license si ya tienes historial local (evita conflictos).
2. En la carpeta del proyecto:

```bash
git status   # revisar que .env no aparezca como archivo nuevo
git remote add origin https://github.com/TU_USUARIO/clawd-clean.git
git branch -M main
git push -u origin main
```

Si aún no tienes commit local: `git add -A && git commit -m "Initial commit: clawd-clean workspace"`, luego el `push`.

**CLI `gh` (opcional):** desde la raíz del repo, `gh repo create clawd-clean --private --source=. --remote=origin --push` crea el repo privado y hace el primer push (requiere `gh auth login`).

### Qué no subir nunca

- `.env`, `.clawdbot/` (estado del gateway), claves en texto claro.
- Revisa antes de cada push si añadiste archivos con tokens (a veces se cuelan en JSON de prueba).
