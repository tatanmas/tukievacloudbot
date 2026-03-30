# Checklist de carga — Tuki (borrador / publicado)

Plantilla hasta que el backend documente el schema oficial de cada POST. **No inventar endpoints**; completar esta tabla con fuentes del repo `backtuki` o OpenAPI.

## Alojamiento (accommodation)

| Campo | Obligatorio | Tipo / notas | Estado API |
|-------|-------------|----------------|------------|
| *(rellenar desde backend)* | | | TODO |

## Experiencia

| Campo | Obligatorio | Tipo / notas | Estado API |
|-------|-------------|----------------|------------|
| *(rellenar desde backend)* | | | TODO |

## Traslado / transporte

| Campo | Obligatorio | Tipo / notas | Estado API |
|-------|-------------|----------------|------------|
| *(rellenar desde backend)* | | | TODO |

## Rent-a-car / centrales

| Campo | Obligatorio | Tipo / notas | Estado API |
|-------|-------------|----------------|------------|
| *(rellenar desde backend)* | | | TODO |

## Flujo deseado (agente)

1. Validar JSON contra este checklist (cuando esté completo).
2. Si falta campo obligatorio → pedirlo a Tatan o crear tarea Notion.
3. Si existe endpoint de creación en borrador → llamar desde script/skill con credenciales adecuadas (no token de integración LLM si es solo lectura).
4. Si solo hay UI → tarea Notion “Publicar manualmente” + enlace a SuperAdmin.

Referencias en repo: `content/tuki/README.md` (estructura de carpetas de contenido), `docs/RED-AGENTES-TUKI-NOTION.md`.
