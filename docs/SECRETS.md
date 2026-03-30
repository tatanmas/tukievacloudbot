# Secretos — qué cargar y qué rotar

## No copiar secretos del repo viejo

En clawd-clean **no** se copian `.env.docker`, `.env.tuki`, ni ningún archivo que contenga tokens o API keys desde el repo anterior (clawd). Todo se carga de nuevo y, si aplica, se rota.

## Qué cargar manualmente en clawd-clean

Crear `.env` a partir de `.env.example` y definir:

| Variable | Uso |
|----------|-----|
| `CLAWDBOT_GATEWAY_TOKEN` | Auth de la Control UI y del chat. Generar nuevo (ej. `openssl rand -hex 24`). |
| `ANTHROPIC_API_KEY` | Claude (primary). |
| `NVIDIA_API_KEY` | Kimi (fallback). |

Opcional más adelante (Fase 2):

- `NOTION_TOKEN`, `NOTION_NOTES_DB_ID`, `NOTION_ACTIONABLES_DB_ID` si usas skill Notion.
- Credenciales WhatsApp si añades canal WhatsApp.

## Qué rotar (por haber estado expuestos)

Si en el repo viejo o en backups llegaron a estar en texto plano o en repos:

- **Token del gateway** — si estaba en `.env.docker` o en algún config versionado: generar uno nuevo y usarlo solo en `.env` de clawd-clean (no commitear).
- **Claves de API** (Anthropic, NVIDIA) — si tienes duda, rota en el dashboard del proveedor y usa las nuevas en `.env`.
- **Notion** — si el token o IDs estuvieron en config o en el sandbox del repo viejo: crear nueva integración en Notion si hace falta y no reutilizar el token viejo en clawd-clean.

## Cómo dejarlos fuera del repo

- **No commitear:** `.env`, `.env.docker`, cualquier archivo con valores reales.
- **Sí commitear:** `.env.example` con placeholders y sin valores reales.
- **.gitignore:** ya incluye `.env`, `.env.*` y excluye solo `!.env.example`.
- No poner tokens en `clawdbot.json`; usar variables de entorno o archivos que estén en `.gitignore`.
