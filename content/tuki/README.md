# Tuki Content - Estructura de Trabajo

Estructura de carpetas para el contenido de operadores.

## Estructura

```
/workspace/content/tuki/
├── operadores/              # Contenido de operadores reales
│   └── {operador_id}/
│       └── {item_id}/
│           ├── fotos/
│           │   ├── principal.jpg
│           │   ├── galeria_01.jpg
│           │   └── ...
│           ├── datos.json
│           └── info_recibida.txt
├── ejemplos_json/           # Ejemplos de schemas para DataModeler
│   ├── ejemplo_alojamiento.json
│   ├── ejemplo_experiencia.json
│   └── ejemplo_traslado.json
└── README.md
```

## Flujo de trabajo

1. **OnboardingAgent** recolecta datos → guarda en `datos.json`
2. **ContentUploader** organiza fotos → carpeta `fotos/`
3. **DataModeler** transforma a JSON final → valida contra schemas
4. Sube a backend Tuki → POST a API

## Campos de datos.json

### Alojamiento
```json
{
  "operador_id": "hotel_xyz",
  "nombre": "Hotel Boutique XYZ",
  "tipo": "alojamiento",
  "categoria": "hotel|hostal|camping|cabana",
  "ubicacion": {
    "direccion": "...",
    "ciudad": "Santiago",
    "pais": "CL"
  },
  "contacto": {
    "email": "...",
    "telefono": "...",
    "whatsapp": "..."
  },
  "precios": {
    "moneda": "CLP",
    "adulto": 50000,
    "nino": 35000
  },
  "fotos_count": 8,
  "estado": "en_proceso|listo_para_subir"
}
```

### Experiencia
```json
{
  "operador_id": "tour_xyz",
  "nombre": "Tour Capital",
  "tipo": "experiencia",
  "categoria": "tour|aventura|gastronomia|cultural",
  "duracion": "4 horas",
  "ubicacion": {
    "ciudad": "Santiago",
    "pais": "CL"
  },
  "contacto": {...},
  "precios": {...},
  "fotos_count": 6,
  "estado": "en_proceso"
}
```
