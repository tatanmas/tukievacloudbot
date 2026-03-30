# Logs del gateway — revisar cuando algo falle

Cuando el chat **se corta, no responde o falla**, la primera acción es mirar los logs del gateway.

## Comando para tener logs en vivo (en una terminal)

Desde la raíz del repo (`clawd-clean`):

```bash
docker compose logs -f clawdbot-gateway
```

- **`-f`** = sigue mostrando líneas nuevas (como `tail -f`). Déjalo corriendo en una terminal.
- Cuando pase algo raro, puedes **referenciar esa terminal** en el chat con Eva/Cursor (ej. “revisa la terminal de logs” o pegar las últimas líneas) para que revise qué pasó.
- Para salir: `Ctrl+C`.

## Ver últimas N líneas (sin seguir)

```bash
docker compose logs clawdbot-gateway --tail 100
```

## Qué buscar en los logs

- **`Embedded agent failed`** o **`lane task error`** → error del modelo o de la API (ej. límite de créditos, timeout).
- **`FailoverError`** → el modelo principal (Claude) falló; puede que el fallback (Kimi) no se haya usado o también falló.
- **`webchat disconnected code=1001`** → el cliente (navegador) cerró la conexión; a veces la UI se corta por eso.
- **`API usage limits`** / **`You will regain access on`** → Anthropic pausó por límite de gasto. Con Kimi como primary (config actual) el chat debería responder con Kimi; si aún falla, ver CREDITS-API.md.
- **`lane enqueue: lane=session:agent:main queueSize=N`** con N creciendo **sin** respuestas nuevas → un run quedó **colgado**; los mensajes solo encolan. **Qué hacer:** `docker compose restart clawdbot-gateway` y **Nueva sesión** (`agent:main:main`). Ver también el log en archivo dentro del contenedor: `/tmp/clawdbot/clawdbot-YYYY-MM-DD.log`.
- **`lane wait exceeded`** / **`announce queue drain failed` / `gateway timeout after 60000ms`** → espera interna > ~25–60 s; run pesado o timeout del gateway.
- **`read failed: ENOENT`** en un `.py` → archivo **no existe** (ruta inventada por el modelo).
- **`python: not found`** → usar `python3` o imagen con symlink `python` → `python3` (clawd-clean Dockerfile).
- **`device signature expired`** (WebSocket `code=1008`) → la **extensión / Control UI** intentó conectar con una firma de dispositivo vieja o sin aprobación. **Qué hacer:** (1) `docker exec clawd-clean-gateway clawdbot devices list` — si hay **Pending**, `clawdbot devices approve <requestId>` dentro del contenedor; (2) mismo **`CLAWDBOT_GATEWAY_TOKEN`** en `.env` y en la extensión; (3) desconectar y volver a conectar la extensión. Detalle: **`TOOLS.md`** § Chrome / Control UI.
- **`[browser/server] Browser control listening on http://127.0.0.1:18791/`** → arrancó el servidor **Express** de control del navegador (puerto **18791**). La **extensión Chrome** debe usar el relay en puerto **18792** (`http://127.0.0.1:18792/`, `GET /` → `OK`). Si la extensión apunta a **18791**, puede fallar el chequeo “Relay not reachable/authenticated”. Ver **`TOOLS.md`** § Chrome.

## Verificación rápida: dispositivos emparejados (sin errores)

Salida **esperada** cuando todo está bien con pairing (ejemplo real):

```bash
docker exec clawd-clean-gateway clawdbot devices list
```

- Debe listar **`Paired (N)`** con al menos los clientes que usas (Control UI desde `172.20.0.1`, CLI opcional desde `127.0.0.1`).
- **`Pending (0)`** (o que no aparezca sección Pending): no hay solicitudes esperando `approve`.
- El aviso **`(node:…) [DEP0040] DeprecationWarning: punycode`** viene de Node/clawdbot; **se puede ignorar**; no indica fallo de pairing.

Si aparece **`Pending (1)`** o más, aprueba con:

`docker exec clawd-clean-gateway clawdbot devices approve <requestId>` (el UUID de la columna Request).

## Por qué no ves el error en el chat

Cuando el agente falla (ej. límite de Anthropic), el gateway **no muestra** ese error en el chat: la sesión embedded falla en silencio y no envía ningún mensaje al usuario (limitación conocida de clawdbot). Por eso a veces solo ves la conversación cortada y nada más. La forma de saber qué pasó es **revisar los logs** (comando de arriba o `docker compose logs clawdbot-gateway --tail 100`). Objetivo a futuro: que el gateway o la UI inyecten el mensaje de error en el chat para no tener que ir a logs.

## Flujo cuando algo falla

1. Tener (o abrir) la terminal con `docker compose logs -f clawdbot-gateway`.
2. Si el chat falló, decir en el chat: “revisa los logs” o “no respondió, mira la terminal de logs” (o pegar las últimas líneas).
3. Quien resuelva (Eva o Cursor) revisa los logs, identifica la causa y propone el siguiente paso (config, nueva sesión, créditos, etc.).
