# Red de agentes Tuki ↔ Notion ↔ métricas

Objetivo: **panorama de plataforma** continuo, **sincronización** entre lo que ya está publicado en Tuki y lo que vive en Notion (leads / operadores), y **automatización del flujo de carga** (borrador → publicado) cuando existan APIs y datos claros.

## Qué ya tenemos en este repo

| Capa | Qué es | Límite |
|------|--------|--------|
| **API integración** | `skills/tuki-integration-api/` → `capabilities`, `snapshot`, `orders/summary` | Solo **GET**, lectura agregada (inventario, órdenes, revenue). No lista uno a uno alojamientos con Notion ID. |
| **Leads en Notion** | `skills/tuki-leads-db/` | CRUD en base “Leads de captación”; estados como *Publicado y operativo*. |
| **Tareas / notas** | `skills/tuki-crm/` | Notion tareas y notas. |
| **Growth** | `docs/GROWTH-EVA.md` | Ritmo de pulso con datos reales. |

## Visión: tres fuentes de verdad

1. **Tuki (producción)** — alojamientos, experiencias, organizadores, traslados, rent-a-car, publicado vs borrador.
2. **Notion (operación)** — leads, seguimiento, backlog, quién es “cliente/operador” en el sentido comercial.
3. **Este workspace (Eva)** — skills, scripts, memoria, prompts; **no** reemplaza al backend.

La **sincronización** no es mágica: hace falta **clave de enlace** (ID de recurso en Tuki guardado en Notion, o slug, o tabla de mapeo) + **lectura** desde Tuki (API o export) + **escritura** en Notion vía `NOTION_TOKEN`.

## Fases recomendadas

### Fase 1 — Panorama y ritmo (ya encaminado)

- **Eva** (o cron en host) ejecuta de forma recurrente:
  - `tuki_api.sh capabilities` → `snapshot` → `orders-summary` (scopes según token).
- Salida: tendencia de inventario, actividad aproximada, revenue elegible (sin inventar métricas).
- **Agente dedicado opcional:** mismo skill + `memory/YYYY-MM-DD.md` con resumen corto (“pulso diario”).

### Fase 2 — Enlace leads ↔ publicados (diseño de datos)

Definir en Notion (propiedades nuevas si hace falta):

- `id_tuki` o `slug_tuki` (texto) — ID o slug del alojamiento/experiencia/organizador en producción.
- `url_admin_tuki` (URL) — link al detalle en SuperAdmin si existe.
- `estado_sync` (select): `sin_enlace`, `en_plataforma`, `discrepancia`, etc.

Regla: **un lead “Publicado y operativo”** debe tener **al menos un enlace** a un recurso real cuando ya está en la plataforma.

### Fase 3 — Sync plataforma → Notion (requiere backend o export)

Para “lo que ya está en la plataforma y no en Notion”:

- **Opción A:** endpoints de **solo lectura** en el backend (lista filtrable de alojamientos/experiencias con `id`, `slug`, `organizer_id`, `status`) consumidos por un script en `skills/` con token adecuado (**no** el mismo contrato que la API integración LLM si el backend separa permisos).
- **Opción B:** export periódico (CSV/JSON) desde admin o job interno → script que **upsert** en Notion (crear página lead mínima o actualizar estado).

Sin esto, el agente solo puede **pedir a un humano** la lista o hacer **cruce manual** por nombre (frágil).

### Fase 4 — Carga JSON alojamiento / experiencia / traslado

Automatizar “subir JSON formateado y quedar en borrador” exige saber:

- **Qué endpoint** acepta creación (POST) y con qué schema (campos obligatorios, enums).
- Si hoy solo existe **UI de SuperAdmin**, el agente puede usar **browser** con pestaña adjunta (más frágil) o **API interna** documentada (preferible).

Hasta que exista API clara, el rol de Eva es: **validar JSON contra checklist**, **crear tarea en Notion**, **no inventar** que ya está subido.

### Fase 5 — Notion como cola de trabajo

- Tareas “Publicar X” con enlace al JSON en `content/tuki/` o adjunto.
- Eva actualiza lead cuando **Tatan confirma** publicación o cuando un script de sync detecta el `id_tuki`.

## Roles de agentes (lógicos)

| Rol | Responsabilidad | Herramientas típicas |
|-----|-----------------|----------------------|
| **Pulso** | Métricas agregadas, snapshot, orders | `tuki-integration-api` |
| **Sync** | Cruce ID/slug Notion ↔ Tuki | Scripts + Notion API + (futuro) API lectura Tuki |
| **Contenido** | Checklist de campos por tipo (alojamiento, experiencia, traslado, coche) | Docs backend + JSON en repo + Notion |
| **Orquestación** | Prioridades, backlog GTD | `tuki-crm`, `MEMORY.md` |

No hace falta “muchas instancias” de Clawdbot al inicio: **un agente Eva** con **skills** y **tareas en Notion** suele bastar; luego se separan sesiones o subagentes si el gateway lo permite.

## Riesgos

- **Duplicar** operadores en Notion si el script crea sin comprobar `id_tuki`.
- **Confundir** lead de prospección con ficha ya publicada (nombres parecidos).
- **Tokens:** integración LLM es lectura; escritura en Tuki requiere otro mecanismo.

---

*Actualizar este doc cuando existan endpoints concretos de listado y de creación en borrador.*
