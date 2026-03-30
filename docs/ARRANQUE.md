# Pasos exactos de arranque — clawd-clean

## Prerrequisitos

- Docker Desktop (Mac) con Docker Compose v2.
- API keys: Anthropic, NVIDIA (para Kimi). Token de gateway (generar nuevo).

## 1. Clonar o usar este directorio

```bash
cd /Users/sebamasretamal/Desktop/cursor/clawd-clean
```

## 2. Variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y definir:

- `CLAWDBOT_GATEWAY_TOKEN` — token seguro (ej. `openssl rand -hex 24`).
- `ANTHROPIC_API_KEY` — clave Anthropic (Claude).
- `NVIDIA_API_KEY` — clave NVIDIA (Kimi fallback).

No commitear `.env`.

## 3. Build de la imagen

```bash
docker compose build
```

## 4. Onboard (solo primera vez)

Genera `.clawdbot/` con config base:

```bash
docker compose run --rm clawdbot-gateway clawdbot onboard
```

Seguir el wizard: elegir agente único `main`, modelos Claude + Kimi, workspace `/workspace`. Si el wizard no pide workspace, editar después `.clawdbot/clawdbot.json` y en `agents.defaults.workspace` y `agents.list[].workspace` poner `/workspace`.

## 5. Ajustar config mínima (si hace falta)

En `.clawdbot/clawdbot.json`:

- `agents.defaults.workspace` → `"/workspace"`
- `agents.list[0].workspace` → `"/workspace"`
- `agents.defaults.model.primary` → `"anthropic/claude-sonnet-4-5"` (o el modelo que uses)
- `agents.defaults.model.fallbacks` → `["nvidia/moonshotai/kimi-k2.5"]`

Guardar. No poner secretos en este archivo; van en `.env`.

## 6. Levantar el gateway

```bash
docker compose up -d
```

## 7. Abrir la UI

1. Navegador: `http://127.0.0.1:18789`
2. Settings → pegar `CLAWDBOT_GATEWAY_TOKEN`.
3. Ir al chat:  
   `http://127.0.0.1:18789/chat?session=agent:main:main&token=TU_TOKEN`  
   (reemplazar `TU_TOKEN` por el valor de `CLAWDBOT_GATEWAY_TOKEN`).

## 8. Copiar contexto migrado (opcional)

**Opción A — Raíz (como pide AGENTS.md hoy):** El agente lee `SOUL.md`, `USER.md`, etc. en la raíz del workspace.

```bash
cp archive/contexto-migrado/SOUL.md archive/contexto-migrado/USER.md archive/contexto-migrado/MEMORY.md archive/contexto-migrado/HEARTBEAT.md archive/contexto-migrado/AGENTS.md .
mkdir -p memory
```

**Opción B — Carpeta de identidad:** Si prefieres que identidad esté en una carpeta (ej. `identity/`), copia ahí y luego edita AGENTS.md para que diga "Read identity/SOUL.md", "Read identity/USER.md", etc.

```bash
mkdir -p identity memory
cp archive/contexto-migrado/SOUL.md archive/contexto-migrado/USER.md archive/contexto-migrado/MEMORY.md archive/contexto-migrado/HEARTBEAT.md identity/
cp archive/contexto-migrado/AGENTS.md .
# Luego editar AGENTS.md y cambiar rutas a identity/SOUL.md, identity/USER.md, identity/MEMORY.md, identity/HEARTBEAT.md
```

Listo. Validación en **VALIDACION.md**. Auditoría de lo hecho y no hecho en **AUDIT-CLAWD-CLEAN.md**.
