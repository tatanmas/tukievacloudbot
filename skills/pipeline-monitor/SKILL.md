# Pipeline Monitor Tuki

Agente maestro que supervisa leads 24/7, genera alertas de estancamiento y mantiene el flujo activo.

## Reglas de Negocio Obligatorias

### Regla 1: Anti-Infinito (Sin movimiento)
```
Lead en "Contactar" por >5 días → ALERTA ROJA
Lead en "Esperando información" por >3 días → ALERTA AMARILLA
Lead en "Esperando respuesta" por >7 días → ALERTA NARANJA
```

### Regla 2: Comunicación Consciente (Notas obligatorias)
```
Lead en estado inactivo >3 días → REQUIERE nota explicativa
Ejemplo: "No contactado porque... | Contactado el X, dijo que... | Volviendo llamar el Y"
```

### Regla 3: SLA de Respuestas
| Tipo | Tiempo máximo | Alerta |
|------|---------------|--------|
| Lead listo "Contactar" | 24 horas | 🔴 Crítica |
| Lead incompleto | 48 horas | 🟡 Media |
| Esperando respuesta cliente | 7 días | 🟠 Seguimiento |

## Alertas Automáticas

### Diarias (Morning Report)
```
📊 Pipeline Report - 2026-03-30
═══════════════════════════════════

🚨 URGENTES (Requieren acción HOY):
├─ Hotel Los Españoles Plus → Contactar hace 5 días
├─ Novotel Providencia → Contactar hace 3 días
└─ Casa Cecilia → Esperando info hace 4 días

📈 Estadísticas:
├─ Tiempo promedio de enriquecimiento: 2.3 días
├─ Tiempo promedio a primera respuesta: 4.1 días
├─ Leads activos: 47
└─ Conversión Contactar→Reu: 23%

📝 Acciones Sugeridas:
1. Contactar Los Españoles (whatsapp +56223345068)
2. Buscar teléfono Casa Cecilia (prioridad alta)
3. Seguimiento Sheraton (pasaron 7 días)
```

### Semanales
```
📈 Weekly Pipeline Review
═══════════════════════════
Leads nuevos esta semana: 34
Leads contactados: 12
Respuestas positivas: 4
Reuniones agendadas: 2

⚠️ Leads en riesgo de muerte (>14 días sin movimiento): 3
[Ver lista completa en Notion]

✅ Recomendación:
Archivar leads sin movimiento >21 días con nota "muerte natural"
```

## Sistema de Notas Obligatorias

### Cuándo requiere nota de contexto:
- [ ] Lead lleva >3 días sin cambio de estado
- [ ] Lead pasó a "Esperando respuesta" (registrar cómo/qué dijeron)
- [ ] Lead rechazado → Registrar por qué
- [ ] Fecha de seguimiento pasó sin acción

### Template de Nota de Contacto:
```
[2026-03-30 14:30] Contacto vía WhatsApp
- Respondió: Sí / No / Contestador
- Interés: Alto / Medio / Bajo
- Próximo paso: Enviar catálogo / Llamar el X / Esperar
- Notas: "Dijo que consultaría con gerente"
```

## Métricas de Pipeline (KPIs)

```yaml
velocidad_pipeline:
  captura_a_contactar: "X días promedio"
  contactar_a_respuesta: "Y días promedio"
  respuesta_a_reu: "Z días promedio"
  
estado_actual:
  nuevos: 5
  incompletos: 8
  contactar: 2
  esperando: 12
  recontactar: 3
  reu_agendada: 4
  
riesgo:
  estancados_7d: 6
  estancados_14d: 2
  sin_seguimiento: 3
```

## Scripts de Automatización

```bash
# Morning check (ejecutar 9am diario)
./scripts/morning_report.sh

# Revisión de estancados (ejecutar cada 2 días)
./scripts/check_stalled.sh --days 5

# Estadísticas semanales (ejecutar domingos)
./scripts/weekly_stats.sh

# Alerta urgente (ejecutar cada hora)
./scripts/urgent_alerts.sh --slack --email
```

## Dashboard de Pipeline

[Ver en tiempo real en Notion: Dashboard Leads Tuki]

## Comandos

```bash
# Ver estado actual del pipeline
make pipeline-status

# Ver leads bloqueados
make blocked-leads

# Forzar actualización de métricas
make refresh-metrics

# Ejecutar alertas manualmente
make alert-urgent
```
