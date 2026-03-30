# Pulso de growth — chat vs cron vs “equipo growth”

## Qué pasó cuando pediste *“pulso de growth de Tuki esta semana”*

Eva (el modelo) ejecutó **tres comandos** en el gateway:

1. `tuki_api.sh capabilities` — manifiesto y reglas (opcional si ya conoces las URLs).
2. `tuki_api.sh snapshot` — inventario, actividad aproximada, destinos.
3. `tuki_api.sh orders-summary` — órdenes y `revenue_eligible`.

Eso es **bajo demanda**: gasta tokens de LLM + tiempo de API, pero **no** corre solo.

## Cómo diseñar monitorización continua (como un equipo de growth)

| Necesidad | Qué usar | Notas |
|-----------|----------|--------|
| **Mismo dato sin depender del chat** | Script **`growth_pulse.sh`** | Llama snapshot + orders y escribe `data/pulses/latest-growth-pulse.md` + JSON en `data/pulses/`. Sin LLM: solo curl + jq. |
| **Cada día / cada hora** | **Cron en el Mac** con `docker exec … growth_pulse.sh` | Igual que `pipeline-monitor` (ver `crontab.mac.example`). |
| **Que Eva te lo narre** | Abrir chat y decir “resume el último pulso” o pegar `latest-growth-pulse.md` | La “inteligencia” es el modelo leyendo el archivo o el JSON. |
| **“Agentes 24/7”** | En la práctica = **jobs programados** + opcional **Slack/email** | No hace falta otro proceso Clawdbot consumiendo créditos todo el día; el cron es barato y estable. |

### Flujo recomendado

1. **Cron** (ej. lun/mié/vie 9:00) → `growth_pulse.sh` → `data/pulses/latest-growth-pulse.md`.
2. **Tú o Eva** leen ese archivo cuando quieras estrategia (no hace falta repetir las llamadas API).
3. **Opcional:** segunda línea en cron que envíe el `.md` a Slack (webhook) o cree una **nota en Notion** vía script (requiere implementar).

### Probar a mano

```bash
docker exec clawd-clean-gateway bash -lc 'cd /workspace/skills/tuki-integration-api/scripts && ./growth_pulse.sh'
```

Archivo principal: `/workspace/data/pulses/latest-growth-pulse.md` (en el host: `data/pulses/` del repo).

### Añadir al crontab del Mac

Ejemplo (ajustar ruta a `docker`):

```cron
# Lunes a viernes 9:00 — pulso growth Tuki
0 9 * * 1-5 /usr/local/bin/docker exec clawd-clean-gateway bash -lc 'cd /workspace/skills/tuki-integration-api/scripts && ./growth_pulse.sh' >> /tmp/tuki-growth-pulse.log 2>&1
```

## Responder a alguien que pide “diseñar el equipo growth”

- **Datos:** API de integración (solo lectura) + en el futuro sync Notion/plataforma (`docs/RED-AGENTES-TUKI-NOTION.md`).
- **Ritmo:** métricas agregadas en archivo + revisión humana o sesión con Eva para interpretación.
- **No es obligatorio** un segundo agente: un **cron + un archivo** ya dan “pulso constante”; Eva aporta **narrativa y preguntas** cuando hablas con ella.
