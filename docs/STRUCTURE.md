# Estructura del repositorio

El workspace es **`/workspace`** dentro del contenedor del gateway; en tu Mac es la raíz de este repo.

## Raíz (convención Clawdbot / Eva)

Estos archivos **siguen en la raíz** a propósito: el agente los referencia por rutas cortas (`SOUL.md`, `AGENTS.md`, etc.).

| Qué | Rol |
|-----|-----|
| `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, `HEARTBEAT.md`, `TOOLS.md` | Identidad, reglas, memoria larga, latidos, notas de herramientas |
| `README.md`, `Dockerfile`, `docker-compose.yml`, `.env.example` | Arranque y despliegue |
| `patches/` | Parches aplicados a la imagen del gateway |
| `clawd/` | Canvas / extras mínimos |
| `skills/` | Skills (herramientas y scripts por dominio) |
| `memory/` | Notas diarias `YYYY-MM-DD.md` |
| `docs/` | Documentación operativa |

No es un error que **README** conviva con **SOUL**: uno es el proyecto; el otro es el contrato del agente.

## Datos y artefactos (fuera de la raíz)

| Ruta | Contenido |
|------|-----------|
| `data/leads/` | JSON / JSONL de leads, batches exportados |
| `data/leads/scraped/` | Salidas de scraping por destino (árboles locales) |
| `archive/contexto-migrado/` | Copias de identidad usadas solo al migrar desde otro entorno |
| `content/tuki/` | Contenido / briefs Tuki no ligados al runtime del bot |
| `vendor/google-maps-scraper/` | Código de terceros (referencia; no es skill propio) |
| `docs/notes/` | Notas sueltas (p. ej. prospector, estado “unicornio”) |

## Qué tocar al mover cosas

- Scripts o skills que lean rutas **fijas** a `data/leads/...` deben actualizarse si cambias nombres.
- Tras mover solo documentación, actualiza enlaces en `docs/ARRANQUE.md` si aplica.
