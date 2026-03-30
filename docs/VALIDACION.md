# Pasos exactos de validación — clawd-clean

## 1. Gateway en marcha

```bash
docker compose ps
```

`clawd-clean-gateway` debe estar `Up`.

## 2. Logs sin errores graves

```bash
docker compose logs --tail 50 clawdbot-gateway
```

No debe haber stack traces ni salidas que indiquen falta de config.

## 3. UI responde

Abrir en el navegador:

- `http://127.0.0.1:18789`

Debe cargar la Control UI del gateway (login o dashboard). No debe ser una página custom (canvas).

## 4. Chat con sesión main

Abrir:

```
http://127.0.0.1:18789/chat?session=agent%3Amain%3Amain&token=TU_TOKEN
```

(sustituir `TU_TOKEN` por el valor de `CLAWDBOT_GATEWAY_TOKEN`).

Comprobar:

- La página es la ruta `/chat` del gateway.
- Se puede escribir un mensaje y enviar.
- El agente `main` responde (Claude primary; si falla, Kimi fallback).

## 5. Modelos

En la respuesta del agente o en la config, confirmar:

- Primary: Claude (anthropic/claude-sonnet-4-5 o el que hayas puesto).
- Fallback: Kimi (nvidia/moonshotai/kimi-k2.5).

## Criterio de éxito

- UI stock funciona.
- Chat principal funciona.
- Claude primary, Kimi fallback.
- No se depende de estado heredado ni de canvas/patches.

Si algo falla, revisar `.env`, `.clawdbot/clawdbot.json` y que el workspace sea `/workspace` dentro del contenedor.
