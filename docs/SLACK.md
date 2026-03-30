# Slack + Clawdbot (clawd-clean)

Objetivo: que **Eva/Clawdbot** hable por Slack (canales, hilos, DM) y sea el centro de notificaciones del asistente.

## Modo recomendado: Socket Mode

No necesitas URL pública ni exponer puertos a Internet. El gateway se conecta a Slack por WebSocket.

### 1. Crear la app en Slack

**Elige una:**

| Opción | Cuándo usarla |
|--------|----------------|
| **From a manifest** | Recomendado: scopes, Socket Mode y eventos quedan bien de entrada. Pega el JSON de abajo (cambia el nombre si quieres). |
| **From scratch** | Si prefieres configurar a mano; luego sigue los pasos 2–4 de esta guía. |

Después de crear la app (por manifest o desde cero), **siempre** falta un paso manual: en **Socket Mode → App-Level Tokens** crear un token con `connections:write` → ese es el `xapp-...` (**`SLACK_APP_TOKEN`**). El manifest activa Socket Mode pero **no** genera ese token por ti.

#### Manifest listo para pegar (From a manifest)

En **Create New App** → **From a manifest** → workspace → pega esto en la pestaña JSON (el nombre visible en Slack es **`display_information.name`** y el del bot en chats es **`bot_user.display_name`**):

```json
{
  "_metadata": {
    "major_version": 2,
    "minor_version": 0
  },
  "display_information": {
    "name": "Eva",
    "description": "Asistente Eva (Clawdbot)",
    "background_color": "#2c2d30"
  },
  "features": {
    "bot_user": {
      "display_name": "Eva",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read",
        "channels:history",
        "channels:read",
        "chat:write",
        "commands",
        "emoji:read",
        "files:read",
        "files:write",
        "groups:history",
        "groups:read",
        "im:history",
        "mpim:history",
        "pins:read",
        "pins:write",
        "reactions:read",
        "reactions:write",
        "users:read"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    },
    "org_deploy_enabled": false,
    "socket_mode_enabled": true,
    "token_rotation_enabled": false
  }
}
```

Luego **Install to Workspace** (OAuth) y sigue desde el paso 2 (token `xapp-...`).

#### Ya tienes la app y se llama “Demo App” (u otro nombre)

El nombre **no** se cambia en Clawdbot ni en `.env`: se cambia en **Slack**:

1. [api.slack.com/apps](https://api.slack.com/apps) → tu app.
2. **App Manifest** (recomendado): edita el JSON y cambia:
   - `display_information.name` → **Eva** (nombre de la app en el menú Apps / configuración).
   - `features.bot_user.display_name` → **Eva** (cómo se ve el **bot** en canales y `@`).
3. **Save** y, si Slack lo pide, **Reinstall to Workspace** para aplicar cambios.
4. Alternativa por UI: **Basic Information** → **App Display Name** / sección del **bot user** → mismo criterio (app vs nombre del bot en conversaciones).

No necesitas nuevos tokens solo por renombrar; los `xoxb` / `xapp` siguen valiendo salvo que Slack te obligue a reinstalar y entonces solo re-confirma el `.env` si algo cambiara.

#### Desde cero (From scratch)

1. [Slack API — Your Apps](https://api.slack.com/apps) → **Create New App** → **From scratch**.
2. Nombre de la app (ej. **`Eva`**) y el workspace.
3. Aplica manualmente los pasos 2–4 de esta guía (Socket Mode, scopes, eventos).

### 2. Activar Socket Mode

En la app: **Settings → Socket Mode** → **ON**.  
Crea un **App-Level Token** con scope **`connections:write`**. Copia el valor (`xapp-...`) → será **`SLACK_APP_TOKEN`**.

### 3. Permisos del bot (OAuth)

**OAuth & Permissions → Scopes → Bot Token Scopes**. Añade al menos:

- `app_mentions:read`, `chat:write`
- `channels:history`, `channels:read`
- `groups:history`, `groups:read` (canales privados, si los usas)
- `im:history`, `mpim:history`, `users:read`
- `reactions:read`, `reactions:write`, `pins:read`, `pins:write`
- `emoji:read`, `files:read`, `files:write`
- `commands` (si usarás slash commands)

**Install to Workspace** y copia el **Bot User OAuth Token** (`xoxb-...`) → **`SLACK_BOT_TOKEN`**.

### 4. Eventos (Event Subscriptions)

**Event Subscriptions → ON**. Con Socket Mode no hace falta Request URL para desarrollo local.

En **Subscribe to bot events** añade, como mínimo:

- `app_mention`
- `message.channels`, `message.groups`, `message.im`, `message.mpim`
- `reaction_added`, `reaction_removed`
- `member_joined_channel`, `member_left_channel`, `channel_rename`
- `pin_added`, `pin_removed`

Guarda los cambios.

### 5. App Home (DM)

**App Home →** activa **Messages Tab** (para poder chatear por DM con el bot).

### 6. Variables en este repo

En `.env` (no commitear):

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

`docker-compose.yml` ya pasa estas variables al contenedor.

### 7. Registrar el canal en Clawdbot

Desde la raíz del repo (con el contenedor usando el mismo `.env`):

```bash
docker compose run --rm clawdbot-gateway clawdbot channels add --channel slack --use-env
```

### 8. Reiniciar el gateway

```bash
docker compose up -d --force-recreate
```

### 9. Probar en Slack

- Invita el bot a un canal: `/invite @NombreDelBot`
- En canales suele responder cuando lo **mencionas** (`@Clawdbot …`). En DM puede bastar con escribir sin mention (según política por defecto).
- Si usas **pairing** en DM y no contesta: revisa `clawdbot pairing` / docs de pairing en [docs.clawd.bot](https://docs.clawd.bot).

### Comprobación

```bash
docker compose exec clawdbot-gateway clawdbot channels list
docker compose exec clawdbot-gateway clawdbot channels status
```

Documentación CLI: [https://docs.clawd.bot/cli/channels](https://docs.clawd.bot/cli/channels)

### Heartbeat (cada 30 min) vs respuestas en Slack

El **heartbeat** del gateway (`agents.defaults.heartbeat`, p. ej. cada **`30m`**) es un **recordatorio interno** para que el agente revise pendientes (inbox, tareas, etc.). **No** es el intervalo entre mensajes en Slack: las respuestas en Slack son **inmediatas** cuando el gateway está en marcha y el mensaje entra al agente.

Para cambiar el intervalo o desactivarlo: edita `agents.defaults.heartbeat` en `.clawdbot/clawdbot.json` (p. ej. `"every": "2h"` o `"every": "0m"` según soporte del esquema para desactivar).

### Si el bot “no escucha” en canales o DM

1. **`clawdbot doctor --fix`** puede dejar `channels.slack.groupPolicy` en **`allowlist`** sin ningún canal en `channels.slack.channels`. En ese caso **ningún canal público/privado pasa** hasta que añadas entradas a la lista o cambies a **`groupPolicy: "open"`** en `.clawdbot/clawdbot.json`.
2. **DM abiertos** (sin pairing): en config hace falta `channels.slack.dm.policy: "open"` y **`allowFrom: ["*"]`** (Clawdbot valida que el wildcard exista).
3. En **canales**, por defecto hace falta **mencionar al bot** (`@Bot …`). Si las menciones no disparan respuesta (nombre del bot, permisos, etc.), se puede poner `channels.slack.requireMention: false` para que responda a **cualquier** mensaje del canal (**más ruidoso** en equipos grandes; en un workspace personal suele ser aceptable).

---

## Notificaciones “solo salida” (scripts, cron)

Si lo que quieres es que **un script** envíe un mensaje a un canal **sin** pasar por la conversación del agente, puedes usar un **Incoming Webhook** de Slack (otra app o la misma con Incoming Webhooks) y `curl` desde `crontab` o skills. Eso es independiente del canal `slack` del gateway; úsalo para alertas batch (ej. reportes del pipeline).

---

## Referencia rápida (config avanzada)

- Variables: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` (Socket Mode).
- Alternativa **HTTP**: `signingSecret`, URL pública y `webhookPath`; solo tiene sentido si el gateway es alcanzable desde Internet.
