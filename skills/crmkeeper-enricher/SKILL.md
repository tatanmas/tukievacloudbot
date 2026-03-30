# CRMKeeper Enricher

Agente especializado en enriquecer leads incompletos con datos faltantes (teléfono, web, dirección, email).

## Flujo de Estados (Pipeline Tuki)

```
Nuevo (capturado) → Incompleto (faltan datos) → Contactar (listo) → Esperando respuesta
                          ↑                          ↓
                    CRMKeeper busca              SalesCloser
```

## Estados

| Estado | Color | Significado | Próxima Acción |
|--------|-------|-------------|----------------|
| **Nuevo** | 🔵 | Recién capturado | CRMKeeper analiza |
| **Incompleto** | 🟠 | Falta teléfono/web/dirección | CRMKeeper enriquece |
| **Contactar** | 🩷 | Datos completos, listo para outreach | SalesCloser contacta |
| **Esperando respuesta** | 🟡 | Mensaje enviado, sin respuesta | Recontactar en X días |
| **Recontactar** | 🟣 | No respondió, segundo intento | SalesCloser reintenta |
| **Reu Agendada** | 🟠 | Reunión programada | Preparar propuesta |
| **Publicado y operativo** | 🟢 | Aliado activo en Tuki | Mantener relación |

## Campos Requeridos para "Contactar"

Mínimo necesario:
- ✅ Nombre del Lead
- ✅ Teléfono de Contacto **O** Email
- ✅ Tipo de cliente (Hotel/Hostal/Experiencia)
- ✅ País

Opcionales pero deseables:
- 🟡 Dirección/Comuna
- 🟡 Web
- 🟡 Google Maps URL

## Tareas del Agente

### 1. Analizar lead "Nuevo"
```
INPUT: Lead con datos básicos de Google Maps
CHECK: ¿Tiene teléfono o email?
  → SI: Cambiar a "Contactar"
  → NO: Cambiar a "Incompleto", agregar nota de qué falta
```

### 2. Enriquecer lead "Incompleto"
```
INPUT: Lead incompleto
ACTION:
  1. Buscar en Google Maps por nombre + ubicación
  2. Extraer: teléfono, web, dirección completa
  3. Actualizar Notion
  4. Cambiar estado a "Contactar" si completó datos
```

### 3. Próxima Acción (campo obligatorio)

Cada lead debe tener en "Acción o comentario":
- **Incompletos**: "Buscar teléfono en web oficial"
- **Contactar**: "Enviar propuesta vía WhatsApp"
- **Esperando**: "Recontactar el [fecha] si no responde"

## Scripts

```bash
# Ejecutar enriquecimiento de leads incompletos
./scripts/enrich_leads.sh --estado Incompleto --limit 10

# Verificar leads sin próxima acción
./scripts/check_next_action.sh
```

## Métricas

- Leads enriquecidos por día
- Tiempo promedio de enriquecimiento
- Tasa de éxito (find phone/web)
