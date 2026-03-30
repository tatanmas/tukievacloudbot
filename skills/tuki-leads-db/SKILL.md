---
name: tuki-leads-db
description: Gestión de leads de captación para Tuki. Trabaja con la base de datos "Leads de captación" en Notion (ID: 303ddd5f-c230-81a3-a2d4-000be9d8a045). Usa cuando necesites consultar leads, filtrar por estado/país/lugar/tipo/interés, crear nuevos leads, actualizar estados, o gestionar el pipeline de prospección.
---

# tuki-leads-db

Skill para gestionar la base de **Leads de captación** de Tuki en Notion. Permite consultar, crear, y actualizar leads de operadores turísticos, hostales, hoteles y experiencias.

## Base de datos

- **Nombre:** Leads de captación
- **ID:** `303ddd5f-c230-81a3-a2d4-000be9d8a045`
- **URL:** https://www.notion.so/303ddd5fc23080879f4bf6f51c7f5ded

## Campos principales

| Campo | Tipo | Opciones/Notas |
|-------|------|----------------|
| Nombre del Leadp | Título | Nombre del contacto/negocio |
| Estado | Status | Contactar, Nuevo, Esperando respuesta, Recontactar, Reu Agendada, Esperando información, Por publicar, Publicado y operativo, Perdido |
| Teléfono de Contacto | Teléfono | WhatsApp preferido |
| Email | Email | |
| Web | URL | Sitio web del negocio |
| Google maps | URL | Link a Maps |
| País | Multi-select | Chile, Argentina, Perú, Colombia, Brasil, México, Estados Unidos, España, Bolivia, Otro |
| Lugar | Multi-select | Viña del mar, Valparaíso, San pedro de atacama, Uyuni, Pucón, Rapa Nui |
| Tipo de cliente | Multi-select | Experiencias, Hostal, Hotel |
| Fuente de Lead | Select | Linkedin (frio), Personal Network, Orgánico, Acercamiento en persona, Web (Frio), Google Maps |
| Interés | Select | Alto, Medio, Bajo |
| Valor Potencial | Número ($) | Valor estimado del negocio |
| Fecha de Contacto | Fecha | |
| Fecha Próximo Seguimiento | Fecha | |
| Responsable | Texto | Quien lleva el lead |
| Notas | Texto largo | Contexto y detalles |
| Acción o comentario | Texto largo | Últimas acciones |

## Scripts disponibles

Solo hay **tres** scripts en `skills/tuki-leads-db/scripts/`:

- `query_leads.py` — consultar
- `create_lead.py` — crear lead
- `update_lead.py` — actualizar

**No existe** `create_task.py` ni otras rutas: si el modelo inventa nombres, fallará con `ENOENT`. Para tareas de backlog Eva/Notion usar otra vía (API Notion con `curl`, MCP, etc.), no este skill.

Todos los scripts requieren la variable de entorno `NOTION_TOKEN`.

### 1. Consultar leads (query_leads.py)

```bash
python3 scripts/query_leads.py [opciones]
```

Opciones de filtro:
- `--estado ESTADO` - Filtrar por estado
- `--pais PAIS` - Filtrar por país
- `--lugar LUGAR` - Filtrar por lugar (Viña del mar, Uyuni, Pucón, etc.)
- `--tipo TIPO` - Filtrar por tipo (Experiencias, Hostal, Hotel)
- `--interes INTERES` - Filtrar por interés (Alto, Medio, Bajo)
- `--fuente FUENTE` - Filtrar por fuente
- `--responsable RESP` - Filtrar por responsable
- `--limit N` - Límite de resultados (default: 100)

**Ejemplos:**

```bash
# Leads en Uyuni que necesitan contacto
NOTION_TOKEN=xxx python3 scripts/query_leads.py --lugar "Uyuni" --estado "Contactar"

# Hoteles en Chile con alto interés
NOTION_TOKEN=xxx python3 scripts/query_leads.py --pais "Chile" --tipo "Hotel" --interes "Alto"

# Leads de Google Maps sin asignar
NOTION_TOKEN=xxx python3 scripts/query_leads.py --fuente "Google Maps" --responsable ""
```

### 2. Crear lead (create_lead.py)

```bash
python3 scripts/create_lead.py --nombre "Nombre" [opciones]
```

Campos opcionales:
- `--telefono TEL` - Teléfono de contacto
- `--email EMAIL` - Correo electrónico
- `--web URL` - Sitio web
- `--maps URL` - URL de Google Maps
- `--pais PAIS` - País(es) separados por coma
- `--lugar LUGAR` - Lugar(es) separados por coma
- `--tipo TIPO` - Tipo de cliente (Experiencias, Hostal, Hotel)
- `--fuente FUENTE` - Fuente del lead
- `--interes INTERES` - Alto/Medio/Bajo (default: Medio)
- `--valor N` - Valor potencial
- `--estado ESTADO` - Estado inicial (default: Nuevo)
- `--notas NOTAS` - Notas iniciales
- `--responsable RESP` - Responsable asignado
- `--fecha-contacto YYYY-MM-DD` - Fecha de contacto

**Ejemplo:**

```bash
NOTION_TOKEN=xxx python3 scripts/create_lead.py \
  --nombre "Hotel Laguna Colorada" \
  --telefono "+591 2 1234567" \
  --email "info@lagunacolorada.com" \
  --pais "Bolivia" \
  --lugar "Uyuni" \
  --tipo "Hotel" \
  --fuente "Google Maps" \
  --interes "Alto" \
  --notas "Hotel popular en el Salar. Buscamos alianza para Paquete Full Day."
```

### 3. Actualizar lead (update_lead.py)

```bash
python3 scripts/update_lead.py --id PAGE_ID [opciones]
```

El ID de página se obtiene de la consulta (campo `id`).

Opciones:
- `--estado ESTADO` - Cambiar estado
- `--interes INTERES` - Actualizar nivel de interés
- `--notas NOTAS` - Reemplazar notas
- `--agregar-nota NOTA` - Agregar nota al final
- `--fecha-seguimiento YYYY-MM-DD` - Programar seguimiento
- `--fecha-contacto YYYY-MM-DD` - Fecha de contacto
- `--responsable RESP` - Asignar responsable
- `--valor N` - Valor potencial

**Ejemplo:**

```bash
# Actualizar estado y agregar nota
NOTION_TOKEN=xxx python3 scripts/update_lead.py \
  --id "abc123-def456" \
  --estado "Reu Agendada" \
  --agregar-nota "Llamada del 15/01: Interesados en reunir. Pendiente enviar propuesta." \
  --fecha-seguimiento "2026-01-20"
```

## Flujos de trabajo comunes

### Pipeline de prospección típico

1. **Nuevo** → Se identifica el lead, se carga a la base
2. **Contactar** → Hay que hacer primer contacto
3. **Esperando respuesta** → Se envió info, esperando feedback
4. **Reu Agendada** → Hay reunión programada
5. **Esperando información** → El lead necesita enviar datos
6. **Por publicar** → Acordamos alianza, falta subir al sistema
7. **Publicado y operativo** → Lead activo en Tuki ✓
8. **Perdido** → No se concretó (se mantiene registro)

### Casos de uso

**Caso 1: Buscar leads pendientes de contacto**
```bash
python3 scripts/query_leads.py --estado "Contactar" --limit 20
```

**Caso 2: Revisar seguimientos de la semana**
```bash
python3 scripts/query_leads.py --estado "Recontactar"
```

**Caso 3: Cargar lead encontrado en Google Maps**
```bash
python3 scripts/create_lead.py \
  --nombre "Experiencia Stargazing Atacama" \
  --telefono "+56 9 1234 5678" \
  --web "https://touratacama.com" \
  --maps "https://maps.google.com/?q=..." \
  --pais "Chile" \
  --lugar "San pedro de atacama" \
  --tipo "Experiencias" \
  --fuente "Google Maps" \
  --interes "Medio" \
  --notas "Tour astronómico. Buenas reviews en Maps."
```

**Caso 4: Actualizar después de llamada**
```bash
python3 scripts/update_lead.py \
  --id "xxx" \
  --estado "Esperando información" \
  --agregar-nota "16/01: Contacto con Pedro. Interesado pero pide tarifas por WhatsApp." \
  --fecha-seguimiento "2026-01-23"
```

## Notas

- Los scripts usan `urllib` y no requieren dependencias externas
- Los IDs de página en Notion tienen el formato UUID (ej: `abc123-def456-...`)
- Para filtrar por múltiples valores en multi_select, el script usa `contains`
- El estado usa el tipo "status" nativo de Notion (con grupos To-do/In progress/Complete)
