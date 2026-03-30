# LeadScout Browser Agent

Agente de captación en tiempo real que escucha la navegación del usuario, detecta leads automáticamente y los clasifica.

## Modo de Operación

### 1. Escucha Continua (via Cron)
Cada 5-10 segundos toma snapshot del navegador adjunto y analiza:
- Hoteles/Hostales (Google Maps, Booking, Airbnb)
- Experiencias turísticas
- Operadores de tours
- Agencias de viaje

### 2. Pipeline de Procesamiento

```
Tatan navega → LeadScout-Browser detecta → Clasifica → LeadProcessor guarda en Notion
                    ↓
              [snapshot] → [análisis] → [extracción datos] → [sessions_send] → [datos crudos]
                                                                                ↓
                                                                   LeadProcessor recibe
                                                                                ↓
                                                                   [valida] → [guarda Notion]
```

### 3. Clasificación Automática

Detecta automáticamente:
- **Hotel**: Palabras clave "hotel", estrellas, rating de Maps
- **Hostal**: "hostal", "hostel", precios bajos
- **Experiencia**: "tour", "excursión", "aventura", "experiencia"
- **Operador**: "agency", "operador", "turismo"
- **Transporte**: "bus", "transfer", "transporte"

### 4. Datos Extraídos

- Nombre del establecimiento
- Tipo (hotel/hostal/experiencia)
- Rating y reseñas
- Precio (si visible)
- Teléfono (si visible)
- Web (si visible)
- Dirección
- Servicios destacados
- URL de Maps

## Comandos

```bash
# Iniciar modo escucha (ejecutar en terminal aparte)
clawdbot sessions spawn --agent-id LeadScout-Browser --task "Escuchar navegación y capturar leads"

# Pipeline completo
./skills/leadscout-browser/run-pipeline.sh
```
