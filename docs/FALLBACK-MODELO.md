# Fallback de modelo (Claude → Kimi) — configuración hexagonal

El cambio de proveedor cuando uno falla es **a nivel de gateway**, no de la LLM. La arquitectura es hexagonal: si un proveedor no responde, el gateway prueba el siguiente sin que el modelo “decida” nada.

## Configuración correcta (según documentación Clawdbot/OpenClaw)

En `.clawdbot/clawdbot.json` (o `~/.openclaw/openclaw.json`):

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["nvidia/moonshotai/kimi-k2.5"]
      }
    }
  }
}
```

- **`primary`:** modelo que se usa primero (siempre Anthropic cuando esté disponible).
- **`fallbacks`:** lista ordenada de modelos a probar si el primary falla. El gateway intenta el siguiente **sin cortar** la petición del usuario.

Referencia: [Model Failover](https://docs.clawd.bot/model-failover), [Gateway configuration](https://docs.clawd.bot/gateway/configuration) (“Choose and configure models”).

## Comportamiento esperado

1. El gateway envía la petición al **primary** (Claude).
2. Si el proveedor devuelve un error considerado **failover-worthy** (rate limit, billing/credits, timeout, auth), el gateway **marca el perfil en cooldown/disabled** y prueba el **siguiente modelo** en `fallbacks` (Kimi).
3. No se pide a la LLM que “pruebe otro modelo”; la decisión es solo del gateway.

Errores que según la doc deberían activar fallback: auth, rate limits (429), timeouts, **billing/credit** (“insufficient credits”, “credit balance too low”). Los “billing disables” marcan el perfil como disabled y rotan al siguiente proveedor/modelo.

## Por qué a veces no pasa a Kimi

En la práctica, el mensaje concreto de Anthropic *“You have reached your specified API usage limits”* a veces **no** dispara el fallback (bug o clasificación del error en la versión actual de clawdbot). Hay issues/PRs en openclaw sobre 429, 402 e `insufficient_quota` que no siempre activaban el fallback.

- **Qué no hacer:** no poner en instrucciones de la LLM cosas del tipo “si falla Claude usa Kimi”. El fallback no va por ahí.
- **Qué hacer:** mantener esta config (primary + fallbacks). En este proyecto se aplica además un parche en build (ver abajo) para que "usage limits" dispare el fallback.

## Parche aplicado en este proyecto (usage limits → fallback)

En la versión stock de clawdbot, el mensaje de Anthropic *"You have reached your specified API usage limits. You will regain access on..."* no siempre se clasifica como error de billing/rate_limit. En este repo se aplica un **parche en build** que añade esos patrones a `ERROR_PATTERNS.billing`:

- **Dónde:** `patches/patch-failover-errors.js`, aplicado en el Dockerfile tras `npm install -g clawdbot@latest`.
- **Qué añade:** "usage limits", "api usage limits", "regain access", "insufficient_quota", "insufficient quota".
- **Efecto:** cuando Anthropic devuelve ese mensaje, el gateway clasifica el error como failover-worthy y prueba automáticamente el siguiente modelo (Kimi) en la misma petición.

Si actualizas la imagen (`docker compose build --no-cache`), el parche se vuelve a aplicar. El script comprueba si ya está aplicado y no duplica.

## Resumen

| Qué | Dónde |
|-----|--------|
| Orden de modelos (primary, luego fallbacks) | `.clawdbot/clawdbot.json` → `agents.defaults.model` |
| Decisión “probar otro proveedor” | Gateway (infra), no la LLM |
| Si el fallback no se dispara con “usage limits” | Parche `patches/patch-failover-errors.js` en build de la imagen |
