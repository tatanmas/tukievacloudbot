# Créditos y límites de API — registro

Documentar aquí cuando se agoten créditos o se pause el uso de una API, para no quedarse con la duda de qué pasó.

## Anthropic (Claude)

- **Límite configurado (org Tuki):** $5.00 USD total monthly API spend.
- **Comportamiento:** Al superar el límite, Anthropic **pausa** el uso hasta medianoche UTC del día 1 del mes siguiente. Recibes email: "further API usage is now paused for your organization until midnight UTC on [fecha]".
- **Fallback:** Siempre **Claude primary**, **Kimi fallback**. Si Claude falla (límite, 429, etc.), el gateway intenta Kimi sin cortar (fallback **hexagonal**, a nivel gateway; ver **FALLBACK-MODELO.md**). En clawdbot hay un bug: el error "API usage limits" a veces no dispara el fallback; si pasa, reportar/actualizar clawdbot. No cambiar el orden (Claude = primary).
- **Re-enable:** En [Alert Settings](https://console.anthropic.com/) puedes subir o quitar el límite para re-activar de inmediato; si no, se re-activa a las 00:00 UTC del 1 del mes siguiente.

### Registro de eventos

| Fecha (UTC) | Qué pasó | Acción |
|-------------|----------|--------|
| 2026-03-17  | Límite $5 alcanzado; API pausada hasta 2026-04-01 00:00 UTC (email Anthropic). | Fallback a Kimi activo en `.clawdbot/clawdbot.json`. Revisar uso en dashboard Anthropic; si se quiere re-activar antes, quitar/ajustar límite en Alert Settings. |

*(Añadir filas cuando vuelva a ocurrir.)*

**Config correcta:** primary = Claude, fallbacks = [Kimi]. Si el fallback no se dispara ante "usage limits", es bug de clawdbot; no invertir el orden.

## Kimi (NVIDIA)

- Uso vía NVIDIA API; sin límite de créditos mensuales tipo Anthropic en este setup (tratar como "infinito" para fallback).
- Si algún día hubiera límite o pausa, anotarlo abajo.

### Registro de eventos

*(Vacío por ahora.)*

---

**Dónde se configura:** `.clawdbot/clawdbot.json` → `agents.defaults.model.primary` y `agents.defaults.model.fallbacks`. No poner API keys en ese archivo; van en `.env`. Detalle hexagonal (gateway, no LLM): **FALLBACK-MODELO.md** (mismo directorio docs/).
