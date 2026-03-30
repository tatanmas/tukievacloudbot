# Auditoría clawd-clean — Qué está hecho y qué no

Documento para revisión por humanos o por otras IAs. Sin afirmaciones falsas.

---

## 1. ¿Quedó todo funcionando perfecto?

**No.** No se ejecutó ni validó el flujo en este entorno.

- **Lo que sí se hizo:** Crear el proyecto `clawd-clean` con Dockerfile stock, docker-compose mínimo, `.env.example`, documentación (ARRANQUE, VALIDACION, SECRETS, NO-MIGRAR, FASE-2) y la carpeta `archive/contexto-migrado/` con copias de SOUL, USER, MEMORY, HEARTBEAT, AGENTS.
- **Lo que no se hizo:** No se corrió `docker compose build`, no se corrió `clawdbot onboard`, no se levantó el gateway ni se abrió la UI en el navegador. Por tanto, **no está comprobado** que la web levante ni que el chat funcione.

**Cómo levantar la nueva web y comprobar que funciona:**

1. `cd /Users/sebamasretamal/Desktop/cursor/clawd-clean`
2. `cp .env.example .env` y rellenar `CLAWDBOT_GATEWAY_TOKEN`, `ANTHROPIC_API_KEY`, `NVIDIA_API_KEY`.
3. `docker compose build`
4. `docker compose run --rm clawdbot-gateway clawdbot onboard` (primera vez; seguir wizard, workspace `/workspace`).
5. Revisar/editar `.clawdbot/clawdbot.json` para que `agents.defaults.workspace` y `agents.list[0].workspace` sean `"/workspace"`.
6. `docker compose up -d`
7. Abrir `http://127.0.0.1:18789`, pegar el token en Settings, luego abrir  
   `http://127.0.0.1:18789/chat?session=agent:main:main&token=TU_TOKEN`.
8. Validar según VALIDACION.md.

Hasta que tú (o un auditor) ejecuten estos pasos y confirmen que la UI y el chat responden, **no se puede afirmar que “quedó todo funcionando perfecto”**.

---

## 2. Por qué SOUL, USER, MEMORY, HEARTBEAT, AGENTS están “en el directorio” y no en una carpeta de identidad

**Origen del diseño:** En el repo original (clawd), el archivo AGENTS.md dice literalmente:

- “This folder is home.”
- “Read `SOUL.md`”, “Read `USER.md`”, “Read `memory/YYYY-MM-DD.md`”, “Read `MEMORY.md`”.

No se usa ninguna ruta tipo `identity/SOUL.md`. Las rutas son relativas al **workspace** (la carpeta “home” del agente). Por tanto, en ese diseño, SOUL, USER, MEMORY, HEARTBEAT y AGENTS viven en la **raíz del workspace**; solo las notas diarias viven en la subcarpeta `memory/`.

**Qué se hizo en clawd-clean:**

- Se creó `archive/contexto-migrado/` como carpeta de **migración**: ahí están las copias de SOUL, USER, MEMORY, HEARTBEAT, AGENTS para no mezclarlas con el resto del proyecto.
- ARRANQUE.md (paso 8) indica **copiar** esos archivos a la **raíz** del proyecto (`cp archive/contexto-migrado/SOUL.md ... .`) para que el agente los vea, porque AGENTS.md sigue diciendo “Read SOUL.md” (en la raíz), no “Read identity/SOUL.md”.

**Consecuencia:** Tras ese copy, SOUL, USER, MEMORY, HEARTBEAT y AGENTS quedan en la misma raíz que README, docker-compose, etc. **No** se introdujo una carpeta dedicada tipo “identidad de la web” o “identity”. La “mejora” fue solo: (1) proyecto nuevo sin patches/canvas/cron/sesiones viejas, (2) contexto reunido en `archive/contexto-migrado/` para migración explícita, (3) documentación clara. La convención de “identidad en la raíz del workspace” se mantuvo igual que en el repo original.

**Si quieres una mejor arquitectura con carpeta de identidad:**

- Crear por ejemplo `identity/` (o `eva/`) y poner ahí SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, y opcionalmente AGENTS.md.
- **Cambiar AGENTS.md** para que en lugar de “Read SOUL.md” diga “Read identity/SOUL.md” (y lo mismo para USER, MEMORY, HEARTBEAT si también van en identity).
- Mantener `memory/` para `memory/YYYY-MM-DD.md` (o referenciar desde identity si lo mueves).
- Así la “identidad de la web” queda en una carpeta específica y el resto del repo (Docker, docs, `archive/contexto-migrado/`) queda separado. Eso no está implementado en lo entregado; es un cambio posterior que puedes auditar e implementar.

---

## 3. Resumen de lo que se hizo (mejoras reales)

| Qué | Detalle |
|-----|--------|
| Proyecto nuevo | `clawd-clean` como directorio hermano de `clawd`, sin reutilizar estado ni config vieja. |
| Docker | Dockerfile sin patch `sandbox-paths.js`, sin entrypoint custom. docker-compose con un solo servicio, montaje `.:/workspace`, sin speaches, sin proxy, sin volumen de sesiones. |
| Config/estado | No se migró `.clawdbot/` ni sesiones; se indica generar uno nuevo con `clawdbot onboard`. |
| Contexto | SOUL, USER, MEMORY, HEARTBEAT, AGENTS copiados a `archive/contexto-migrado/`; uso opcional copiándolos a la raíz (paso 8 de ARRANQUE). |
| Repo viejo | Contenido antiguo movido a `clawd/_legacy/` (incl. .clawdbot, canvas, docker, scripts, docs de auditorías). |
| Documentación | ARRANQUE, VALIDACION, SECRETS, NO-MIGRAR, FASE-2-CRECIMIENTO; PLAN-CLAWD-CLEAN en el repo clawd. |
| Ubicación de identidad | No se creó carpeta “identidad”; se respetó la convención del AGENTS.md original (archivos en raíz del workspace). |

---

## 4. Cómo partir de nuevo con la mejor arquitectura

1. **Validar la base:** Ejecutar los pasos de ARRANQUE y VALIDACION hasta confirmar que la web y el chat funcionan.
2. **Opcional – carpeta de identidad:** Introducir `identity/` (o similar), mover SOUL, USER, MEMORY, HEARTBEAT (y si quieres AGENTS) ahí, y actualizar AGENTS.md con las rutas `identity/...`.
3. **Crecimiento controlado:** Seguir FASE-2-CRECIMIENTO.md para WhatsApp, cron, Notion, skills, sandbox, sin reimportar estado ni hacks del repo viejo.

---

*Este documento refleja con precisión lo implementado y lo no implementado, para que una auditoría externa pueda comprobarlo.*
