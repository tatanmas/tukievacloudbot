# MEMORY.md - Memorias a largo plazo

## Sistema de trabajo con Tatan

**REGLA CRÍTICA: Usar GTD en Notion para TODO trabajo**

- **Todo** lo que vaya a hacer → agregarlo antes a mi backlog (base de tareas, contexto "Eva" o "Eva Backlog"). Nombre = acción concreta (verbo + objeto).
- **Mientras lo implemento** → poner la tarea en estado **Implementando** (o Ejecutando).
- **Al completar** → marcar ✅ y **comentar** en la tarea qué se hizo, si hace falta (resumen para registro).
- No ejecutar sin tarea en backlog; no dejar en "Implementando" cuando ya terminé.
- Si es recurrente → crear siguiente tarea inmediatamente.
- Bases: accionables → "tareas", no accionables → "notas"
- Contextos: "Eva" (activo) y "Eva backlog" (pendiente)

## API y créditos (Claude / Kimi)

- **Claude (Anthropic):** Siempre **primary**. Si falla o se acaban créditos → el gateway debe **intentar Claude y, si falla, pasar a Kimi** sin cortarse (fallback en `.clawdbot/clawdbot.json`). No invertir el orden: Anthropic principal, Kimi fallback.
- **Registro:** Cuando se agoten créditos o llegue el email de Anthropic, anotar en **CREDITS-API.md** (fecha, qué pasó, acción) para poder revisar después y no quedarse con la duda.

## IDs de Notion
- Base de notas: `edfeb377-32fd-4636-bf68-bf6252a04c64`
- Base de tareas: `9b6a3ee2-05ab-4e47-bc13-a401de09a900`
- **NOTION_TOKEN:** está en **`.env`** (raíz del repo = `/workspace/.env` en el contenedor). No está "faltando": si un exec dice "No hay API key de Notion", recordar que la key está en .env y que hay que **reiniciar el gateway** (`docker compose up -d --force-recreate`) para que el proceso exec la reciba.

## Cómo hacer las cosas (NO pensar cada vez)

### Cuando me pidan el backlog de alguien:
→ Query a Notion, base de tareas, filtrar por contexto correspondiente, estado ≠ ✅
- Contextos conocidos: Eva, Eva Backlog, Cris, Cris Backlog, Tatan, Diego, etc.

### Cuando me pidan crear una nota:
→ POST a Notion, base de notas, con:
- Title: título de la nota
- Tipo: tags apropiados (reunión, Core Tuki, documento, Mentoring, idea, etc.)
- Personas: quién está involucrado
- Contenido en children (bloques)

### Cuando me pidan tareas (o cuando yo vaya a hacer algo):
→ Crear/agregar la tarea al backlog (contexto "Eva" o "Eva Backlog")
→ Pasar a **Implementando** (o Ejecutando) cuando la esté haciendo
→ Al terminar: marcar ✅ y comentar en la tarea qué se hizo si hace falta

## Personas clave

### Patricio Lecaros
- Mentor de Tatan
- Reunión 17/03/2026: planteó los dos caminos (chico vs grande/unicornio)
- Tarea pendiente: plan a 2 años si quiere camino grande

### Cristóbal (Cris)
- Contexto "Cris" en Notion
- Tiene tareas relacionadas con Tuki: Uyuni, Los Molles, guías, operadores

## Comportamiento en chat (gateway dashboard)

- **Tras exec/tool:** Nunca terminar el turno solo con "Completed". Siempre escribir en el mismo mensaje una respuesta en lenguaje natural (qué pasó, qué sigue). Si el sistema corta la respuesta tras un exec, es un fallo de flujo; la intención es que siempre haya texto después del resultado. (Incidente 17/03/2026.)

## API Tuki (integración operativa)

- Skill **`tuki-integration-api`**: solo GET; token **`TUKI_INTEGRATION_TOKEN`** en `.env`; script `skills/tuki-integration-api/scripts/tuki_api.sh`; flujo **capabilities → snapshot / orders-summary** según scopes del token. En prod el Bearer `tuki_...` ya no pasa por SimpleJWT en esas rutas (fix backend).

## Notas
*(Espacio para lo que vayas aprendiendo: qué le molesta, qué le motiva, preferencias de comunicación, etc.)*

---
*Actualizado: 2026-03-30*
