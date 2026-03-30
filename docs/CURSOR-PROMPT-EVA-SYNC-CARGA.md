# Prompt para Cursor — Eva: sync Notion ↔ Tuki y flujo de carga

Copia el bloque entre `<PROMPT>` y `</PROMPT>` en un chat de Cursor en el repo **tukievacloudbot** (workspace `clawd-clean`), o adáptalo por tarea.

---

<PROMPT>

Eres el asistente de código en el workspace de Eva (Clawdbot / Tuki). Objetivos:

1. **Red operativa**
   - Extender o crear skills bajo `skills/` que permitan: (a) pulso periódico de métricas vía `skills/tuki-integration-api/scripts/tuki_api.sh` (capabilities → snapshot → orders-summary); (b) preparar scripts que *cuando existan endpoints* lean listados de alojamientos, experiencias, organizadores, traslados y rent-a-car desde el backend Tuki usando variables de entorno seguras (nunca commitear secretos).
   - Documentar en `SKILL.md` cada skill: cuándo usarlo, límites (solo lectura vs futura escritura), y dependencias (`NOTION_TOKEN`, `TUKI_INTEGRATION_TOKEN`, etc.).

2. **Sincronización Notion ↔ plataforma**
   - La base de leads está en Notion (`skills/tuki-leads-db/SKILL.md` con ID de DB).
   - Diseñar propuesta de campos en Notion: `id_tuki` o `slug_tuki`, `tipo_recurso` (alojamiento | experiencia | organizador | …), `estado_sync`, para que lo publicado en Tuki quede reflejado y los leads “Publicado y operativo” no queden huérfanos de datos.
   - Implementar scripts Python o shell que: lean snapshot agregado si basta, o lean CSV/export si el usuario lo deposita en `data/`; actualicen Notion vía API Notion (como `tuki-crm/scripts/notion_task.py`) con **idempotencia** (no duplicar por nombre ambiguo).

3. **Flujo de carga JSON (alojamiento / experiencia / traslado)**
   - Crear `docs/CHECKLIST-CARGA-TUKI.md` (o similar) con tablas: **campos obligatorios** por tipo de recurso, valores enum si los conoces del backend, y estado esperado (borrador vs publicado). Si no tienes el schema oficial, deja TODOs explícitos y referencias a archivos del backend que el equipo deba pegar.
   - No inventar endpoints POST: si no existen en el repo, documentar “pendiente API backend” y sugerir que Eva solo valide JSON + cree tarea Notion hasta que exista API.

4. **Seguridad**
   - Nunca commitear `.env`; usar `.env.example` con placeholders.
   - No usar `web_fetch` a `api.notion.com` sin token; usar `exec` o scripts que hereden `NOTION_TOKEN` del contenedor gateway.

5. **Estilo**
   - Cambios mínimos y enfocados; seguir estilo existente de `skills/tuki-leads-db` y `tuki-integration-api`.
   - Actualizar `docs/RED-AGENTES-TUKI-NOTION.md` solo si cambias la arquitectura acordada.

Entrega: lista de archivos creados/modificados, y cómo probar cada script con `docker exec clawd-clean-gateway` desde `/workspace`.

</PROMPT>

---

## Cómo usarlo

1. Abre Cursor en la carpeta del repo clonado.
2. Pega el contenido dentro de `<PROMPT>…</PROMPT>` (sin las etiquetas si el chat no las necesita).
3. Añade una línea concreta al final, por ejemplo: *“Prioriza solo el checklist de campos para alojamiento y el script stub de sync Notion.”*

Eva en el **gateway** no “aprende” sola leyendo este archivo: hay que **implementar** skills y, si quieres, una línea en `AGENTS.md` o `TOOLS.md` que diga *“para sync y carga, leer `docs/CURSOR-PROMPT-EVA-SYNC-CARGA.md` y los skills nuevos”*.
