# Cron Tuki / pipeline-monitor — dónde corre

## Por qué `crontab crontab.tuki` en el Mac no sirve tal cual

El archivo `crontab.tuki` usa rutas como `/workspace/skills/...`. Esa ruta es el **workspace montado dentro del contenedor** del gateway (`clawd-clean-gateway`). En macOS **no existe** `/workspace`, así que el cron del sistema no encuentra los scripts.

El agente que dijo *"crontab /workspace/crontab.tuki"* asumía **entorno Linux dentro del contenedor**, no tu Terminal del Mac.

## Opción recomendada: cron en el Mac + `docker exec`

1. **Comprobá el nombre del contenedor:**

   ```bash
   docker ps --filter name=clawd --format '{{.Names}}'
   ```

   Debería ser `clawd-clean-gateway`.

2. **Probá un job a mano** (sin cron):

   ```bash
   docker exec clawd-clean-gateway bash -lc 'cd /workspace/skills/pipeline-monitor && ./morning_report.sh'
   ```

   Si ves el reporte en pantalla y no errores, el entorno (Notion, etc.) está bien dentro del contenedor.

3. **Instalá entradas en crontab del Mac** usando el mismo patrón. Ejemplo copiado de `crontab.mac.example`:

   ```bash
   crontab -e
   ```

   Pegá líneas como (ajustá la ruta de `docker` si `which docker` no es `/usr/local/bin/docker`):

   ```cron
   0 9 * * * /usr/local/bin/docker exec clawd-clean-gateway bash -lc 'cd /workspace/skills/pipeline-monitor && ./morning_report.sh' >> /tmp/tuki-morning.log 2>&1
   ```

4. **Listado y logs:**

   ```bash
   crontab -l
   tail -f /tmp/tuki-morning.log
   ```

**Nota:** Docker Desktop tiene que estar **corriendo** y el contenedor **arriba** cuando dispare el cron; si el Mac está apagado o Docker parado, esa ejecución se pierde.

## Opción alternativa: cron/job dentro del propio Clawdbot

Si en el futuro usás `clawdbot cron` en el host o jobs en la UI, eso es otro canal (ver estado en `.clawdbot/cron/`). No es lo mismo que `crontab.tuki` del repo.

## Resumen

| Dónde | `crontab.tuki` con `/workspace/...` |
|-------|-------------------------------------|
| Dentro del contenedor (avanzado) | Válido si copiás el archivo ahí y tenés `cron` instalado en la imagen (hoy la imagen **no** trae cron por defecto). |
| macOS | **No** — usá `crontab.mac.example` + `docker exec`. |
