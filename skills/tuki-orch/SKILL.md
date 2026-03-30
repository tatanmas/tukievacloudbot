---
name: tuki-orch
description: Orquestador maestro 24/7 del ecosistema de agentes Tuki. Coordina LeadScout, CRMKeeper, SalesCloser y agentes especializados para captación continua de leads.
---

# Tuki Orquestador (Unicorn Mode)

Sistema de orquestación autónoma que mantiene todos los agentes trabajando 24/7 para transformar Tuki en una máquina de captación de leads.

## Arquitectura 24/7

### Agentes Base (existentes)
| Agente | SessionKey | Rol | Frecuencia |
|--------|------------|-----|------------|
| CRMKeeper | 78f28d72-1716-4361-bd46-dd5d1400a4c3 | Limpieza de datos | Cada 6h |
| LeadScout | fd1c1a22-84af-4ca6-abb1-777126db11a9 | Prospección general | Cada 2h |
| SalesCloser | 2d3792a0-1de8-427a-b286-c27318c76935 | Outreach WhatsApp | Cada 4h |

### Agentes Destino (nuevos - multi-scraping)
Cada destino tiene su propio LeadScout especializado:
- `LeadScout-SCL` → Santiago, Valparaíso, Viña
- `LeadScout-PUC` → Pucón, Villarrica, Temuco
- `LeadScout-ATA` → San Pedro, Calama
- `LeadScout-CAR` → Carretera Austral, Coyhaique
- `LeadScout-BRA` → Río, Ilha Grande, Paraty
- `LeadScout-BOL` → Uyuni, La Paz

### Agentes Pipeline (nuevos - cierre-loop)
- `OnboardingAgent` → Post-contacto a datos recibidos
- `ContentProcessor` → Organizar fotos/datos de operadores
- `DealCloser` → Negociación y cierre de alianzas

## Flujo de Orquestación 24/7

```
Hora 0:00 ──► LeadScout-SCL (scrapea Santiago)
       │
Hora 0:02 ──► LeadScout-PUC (scrapea Pucón)
       │
Hora 0:04 ──► CRMKeeper (limpia leads de últimas 6h)
       │
Hora 0:30 ──► SalesCloser (contacta leads "Contactar")
       │
Hora 2:00 ──► LeadScout-SCL (segunda ronda)
       │
Hora 4:00 ──► LeadScout-ATA (scrapea Atacama)
       │
Hora 4:00 ──► SalesCloser (follow-ups)
       │
... (continúa)
```

## Scripts de Orquestación

### 1..spawn_leadscout_destino.sh
Crea agentes LeadScout especializados por destino.

```bash
./scripts/spawn_leadscout_destino.sh SCL "Santiago" "Hostal,Hotel"
./scripts/spawn_leadscout_destino.sh PUC "Pucón" "Experiencias,Hostal"
./scripts/spawn_leadscout_destino.sh ATA "San Pedro de Atacama" "Experiencias,Hotel"
```

### 2. run_orquestador.sh
Script maestro que ejecuta cada X horas:

```bash
#!/bin/bash
# run_orquestador.sh - Ejecutar cada 2 horas via cron

# 1. Revisar qué agentes están activos
# 2. Spawnear los que no estén corriendo
# 3. Asignar leads a SalesCloser si hay backlog
# 4. Reportar métricas
```

### 3. check_health.sh
Monitorea estado de todos los agentes:

```bash
./scripts/check_health.sh
# Output:
# ✓ CRMKeeper: última actividad 2h ago
# ✓ LeadScout-SCL: scraping en progreso
# ✗ LeadScout-PUC: dormido >6h, reactivando...
```

## Métricas Unicornio

Seguimiento continuo de KPIs:

| Métrica | Meta diaria | Actual |
|---------|-------------|--------|
| Leads descubiertos | 50 | - |
| Leads contactados | 20 | - |
| Respuestas positivas | 5 | - |
| Reuniones agendadas | 2 | - |
| Alianzas cerradas | 1 | - |

## Cron Jobs (configurar)

```bash
# Cada 2 horas: spawn orquestador
0 */2 * * * cd /workspace && ./skills/tuki-orch/scripts/run_orquestador.sh

# Cada 6 horas: reporte de métricas
0 6,12,18 * * * cd /workspace && ./skills/tuki-orch/scripts/report_metrics.sh

# Cada hora: health check
0 * * * * cd /workspace && ./skills/tuki-orch/scripts/check_health.sh
```

## Comandos Rápidos

```bash
# Activar modo unicornio (todos los agentes)
make unicorn-mode

# Pausar todos los agentes
make pause-all

# Ver dashboard de métricas
make dashboard

# Spawnear agente de un destino específico
python3 scripts/spawn_agent.py --destino SCL --tipo "Hostal"
```
