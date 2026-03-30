# Skills en Docker (sin Homebrew)

La **Control UI** a veces muestra “Install … (brew)”. Eso asume un **Mac con Homebrew**. El gateway de **clawd-clean** corre en **Linux dentro de Docker**: ahí **no hay `brew`** y **no hace falta**.

## Qué ya va en la imagen

En el **`Dockerfile`** se instalan binarios oficiales para Linux (**amd64** y **arm64**):

| Binario   | Skill / uso              | Variable de entorno principal      |
|-----------|--------------------------|------------------------------------|
| `goplaces`| Google Places API (New)  | `GOOGLE_PLACES_API_KEY` (en `.env` + Compose) |
| `gog`     | Google Workspace (CLI)   | OAuth en disco (ver abajo)         |

Tras `docker compose build` y `up`, comprueba dentro del contenedor:

```bash
docker exec clawd-clean-gateway goplaces --version
docker exec clawd-clean-gateway gog version
```

## Google Places (`goplaces`)

1. En [Google Cloud Console](https://console.cloud.google.com/) crea un proyecto y habilita **Places API (New)**.
2. Crea una API key y restrínjela (HTTP referrers / IPs) según tu política.
3. Pon la clave en **`.env`**:
   ```bash
   GOOGLE_PLACES_API_KEY=tu_clave
   ```
4. `docker compose up -d --force-recreate` para que el gateway herede la variable en **exec**.

Prueba:

```bash
docker exec clawd-clean-gateway sh -c 'goplaces search "café" --limit 2 --json'
```

(Sin key válida fallará la API; eso ya es cuota/restricciones de Google.)

## Google Workspace (`gog`)

`gog` necesita **OAuth** (navegador) la primera vez. Opciones:

- **`docker exec -it`** al contenedor y seguir la guía del skill (`gog auth credentials …`, `gog auth add …`). Los tokens suelen guardarse bajo el **HOME** del proceso (en este stack `HOME=/workspace`), es decir **persisten en tu repo montado** si el CLI escribe ahí.
- O preparar credenciales en el Mac y **montar** solo la carpeta de config (avanzado).

Sin completar OAuth, el binario existe pero el skill seguirá “incompleto” para Gmail/Calendar/etc.

## Otros skills “blocked”

- **`gifgrep`** / **`himalaya`** / etc.: suelen depender de otro binario o de **macOS**. Para usarlos en Docker habría que añadir el binario Linux equivalente al `Dockerfile` (como con `goplaces`) o no usarlos en este entorno.
- **`local-places`**: no es solo un binario; levanta un servidor Python con **`uv`**. Es otro nivel de complejidad; para mapas suele bastar **`goplaces`** con la API key.
- **Navegación web / `web_fetch`**: no se arregla con `brew`; depende de la config del gateway y de tokens del proveedor (si aplica). **Notion** va mejor con **exec + `curl` + `NOTION_TOKEN`** (ver `TOOLS.md`).

## Resumen

- **100% funcional** para tu caso “Google Maps / Places” en Docker = **`goplaces` + `GOOGLE_PLACES_API_KEY`** (ya cableado en la imagen y en `docker-compose.yml`).
- **`brew`** en el contenedor no es el camino: **binarios Linux + `apt`** (y variables en `.env`) sí.
