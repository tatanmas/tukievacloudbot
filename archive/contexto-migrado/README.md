# ¿Por qué hay SOUL/AGENTS aquí **y** en la raíz?

- **Raíz del repo** (`/workspace/SOUL.md`, `AGENTS.md`, …): es lo que **Clawdbot / Eva lee en cada sesión**. Convención documentada en [OpenClaw workspace](https://open-claw.bot/docs/workspace): esos archivos viven en la **raíz del workspace**, no dentro de una subcarpeta.
- **`archive/contexto-migrado/`**: copias guardadas al **migrar** desde otro entorno (backup / referencia). No son el “segundo lugar” donde el agente busca; son **histórico o plantilla**.

Si el contenido es **idéntico** a la raíz, es normal: se copiaron en un momento dado y luego editaste solo la raíz (o ambos quedaron igual). Puedes:

- **Dejar** esta carpeta como archivo histórico, o  
- **Borrar** lo que ya no necesites comparar, para no duplicar ruido en el repo.

No hay una regla de internet que obligue a mantener dos copias; la práctica recomendada es **una fuente de verdad en la raíz** para el agente.
