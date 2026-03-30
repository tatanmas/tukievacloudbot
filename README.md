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

Documentación del proyecto en **docs/**: `docs/ARRANQUE.md`, `docs/VALIDACION.md`, `docs/SECRETS.md`, `docs/SLACK.md` (conectar Clawdbot a Slack), `docs/FASE-2-CRECIMIENTO.md`, `docs/CREDITS-API.md`, `docs/FALLBACK-MODELO.md` (fallback hexagonal gateway), `docs/LOGS.md`, **`docs/STRUCTURE.md`** (árbol de carpetas), **`docs/GROWTH-EVA.md`** (Eva + Tuki API + Notion para growth), **`docs/PULSO-GROWTH-CRON.md`** (cron + pulso automático vs chat), **`docs/RED-AGENTES-TUKI-NOTION.md`** (red de agentes, sync Notion ↔ plataforma, fases), **`docs/CURSOR-PROMPT-EVA-SYNC-CARGA.md`** (prompt para Cursor), **`docs/CHECKLIST-CARGA-TUKI.md`** (plantilla checklist de carga).

**Nota:** `SOUL.md`, `AGENTS.md`, `memory/`, `skills/` en la raíz **no** es desorden: es la convención del workspace Clawdbot. Lo que era “ruido” (leads, vendor, migración) quedó bajo `data/`, `vendor/`, `archive/`.

## Repositorio en GitHub

- **Remoto:** `git@github.com:tatanmas/tukievacloudbot.git`
- **Web:** https://github.com/tatanmas/tukievacloudbot

Este workspace versiona **skills**, `AGENTS.md`, `docker-compose`, parches y documentación, sin secretos (`.env` en `.gitignore`; solo `.env.example`).

### Clonar en otra máquina

```bash
git clone git@github.com:tatanmas/tukievacloudbot.git
cd tukievacloudbot
cp .env.example .env   # y completar valores locales
```

### Primer push en un clon nuevo (si aplica)

```bash
git remote add origin git@github.com:tatanmas/tukievacloudbot.git
git branch -M main
git push -u origin main
```

### Qué no subir nunca

- `.env`, `.clawdbot/` (estado del gateway), claves en texto claro.
- Revisa antes de cada push si añadiste archivos con tokens (a veces se cuelan en JSON de prueba).
