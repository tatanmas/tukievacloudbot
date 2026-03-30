# Fase 2 — Crecimiento controlado (después de validar la base)

Solo añadir cada bloque cuando la base (UI stock, chat main, Claude + Kimi) funcione y esté validada.

## 1. WhatsApp

- Habilitar plugin/channel WhatsApp en la config de Clawdbot.
- Añadir credenciales en `.env` (o en el mecanismo que use el gateway) y no commitearlas.
- Documentar en este repo los pasos (cuenta, dispositivo, allowlist) para no repetir desastres.

## 2. Cron

- Definir jobs en un JSON o en la config.
- Registrar con `clawdbot cron` desde el host o desde el contenedor, según documentación actual.
- No reutilizar `cron-jobs-tuki.json` ni el entrypoint que hacía cron-sync del repo viejo; reintroducir cron desde cero y documentar.

## 3. Notion / Tuki

- Skill Notion: configurar con `NOTION_TOKEN` y IDs de bases en env; añadir skill al agente si aplica.
- Tuki (backend, integraciones): añadir como skills propias cuando la base estable lo permita; credenciales en env, no en repo.

## 4. Skills

- Revisar qué skills del repo viejo son realmente útiles (notion, eva-monitor, etc.).
- Copiar solo la skill (carpeta + SKILL.md), no el estado ni config antigua.
- Probar cada skill en clawd-clean con config mínima antes de dejarla fija.

## 5. Sandbox extendido

- Si se necesita sandbox con más herramientas (curl, node, python, jq), construir una imagen tipo `Dockerfile.sandbox` y referenciarla en la config del agente.
- No reintroducir el patch `sandbox-paths.js` salvo que sea estrictamente necesario y esté documentado; preferir configuración stock cuando exista.

---

Orden recomendado: validar base → luego WhatsApp o Notion (según prioridad) → cron → resto de skills y sandbox. Cada paso documentado en este repo para no repetir el desastre del entorno viejo.
