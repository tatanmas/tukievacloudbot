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
- **`API usage limits`** / **`You will regain access on`** → Anthropic pausó por límite de gasto. El fallback a Kimi debería activarse; si no (chat cortado), es bug conocido de clawdbot con ese tipo de error. Ver CREDITS-API.md.
- **`lane enqueue: lane=session:agent:main queueSize=N`** con N creciendo (2, 3, 4…) **sin** nuevos `embedded run start` / respuesta en el chat → el **primer run de esa sesión quedó colgado** (a menudo esperando al LLM después de tools). Los mensajes nuevos **solo encolan**. Mientras tanto solo verás `webchat connected/disconnected` y RPCs tipo `config.schema`. **Qué hacer:** `docker compose restart clawdbot-gateway` (o `up -d --force-recreate`) y abrir **Nueva sesión** con `session=agent:main:main`. Detalle DEBUG en el archivo de log del gateway (ver abajo).
- **`lane wait exceeded: lane=session:agent:main waitedMs=…`** → el cliente esperó demasiado a que la sesión procese (run largo o cola bloqueada).
- **`announce queue drain failed` / `gateway timeout after 60000ms`** → operación interna del gateway superó **60 s** (run muy pesado, modelo lento, o bloqueo). Puede cortar la sensación de “sigue respondiendo” aunque luego el modelo termine en background.
- **`read failed: ENOENT` … script** → ruta/archivo **no existe** (modelo inventó nombre, ej. `create_task.py`). Corregir ruta o crear el archivo.
- **`python: not found`** (exec) → en la imagen solo hay **`python3`** salvo que exista symlink `python` → en clawd-clean el Dockerfile enlaza `python` → `python3`.

## Log en archivo (más detalle que `docker compose logs`)

Dentro del contenedor el gateway también escribe en **`/tmp/clawdbot/clawdbot-YYYY-MM-DD.log`** (línea `log file:` al arrancar). Ahí suelen aparecer `embedded run start`, `tool start/end`, `run active check`, etc., aunque en stdout solo salga el WebSocket.

## Por qué no ves el error en el chat

Cuando el agente falla (ej. límite de Anthropic), el gateway **no muestra** ese error en el chat: la sesión embedded falla en silencio y no envía ningún mensaje al usuario (limitación conocida de clawdbot). Por eso a veces solo ves la conversación cortada y nada más. La forma de saber qué pasó es **revisar los logs** (comando de arriba o `docker compose logs clawdbot-gateway --tail 100`). Objetivo a futuro: que el gateway o la UI inyecten el mensaje de error en el chat para no tener que ir a logs.

## Flujo cuando algo falla

1. Tener (o abrir) la terminal con `docker compose logs -f clawdbot-gateway`.
2. Si el chat falló, decir en el chat: “revisa los logs” o “no respondió, mira la terminal de logs” (o pegar las últimas líneas).
3. Quien resuelva (Eva o Cursor) revisa los logs, identifica la causa y propone el siguiente paso (config, nueva sesión, créditos, etc.).
