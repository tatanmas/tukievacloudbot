# CRMKeeper Deduper

Agente anti-duplicados. Busca y elimina leads repetidos en Notion manteniendo el más completo.

## Reglas de Duplicado

### Nivel 1: Coincidencia exacta (100%)
- Nombre del Lead igual (ignorando mayúsculas/espacios)
- Mismo teléfono
- Misma ciudad/comuna

### Nivel 2: Probable (80%)
- Nombre similar
- Misma ubicación
- Mismo tipo (hotel/hostal)

### Nivel 3: Revisar manual
- Variaciones de nombre
- Misma dirección diferente nombre

## Acciones sobre Duplicados

```
DETECTAR duplicado → COMPARAR campos → MANTENER el más completo → ARCHIVAR/ELIMINAR
```

| Criterio | Peso |
|----------|------|
| Tiene teléfono | +10 |
| Tiene email | +8 |
| Tiene web | +6 |
| Tiene dirección completa | +5 |
| Tiene Google Maps URL | +4 |
| Más notas/detalles | +3 |
| Fecha más reciente | +2 |

## Flujo Prevención (en LeadScout)

```
Nuevo lead detectado → BUSCAR en Notion → ¿Existe?
  → SI → Actualizar existente (no crear nuevo)
  → NO → Crear nuevo lead
```

## Scripts

```bash
# Buscar duplicados
./scripts/find_duplicates.sh

# Comparar y fusionar leads específicos
./scripts/merge_leads.sh lead_id_1 lead_id_2

# Ejecutar dedup automático
./scripts/dedup_daily.sh
```

## Métricas

- Duplicados detectados
- Fusiones realizadas
- Prevenciones (duplicados evitados)
