#!/bin/bash
# LeadScout Browser Pipeline - Modo Tiempo Real
# Ejecutar: ./run-pipeline.sh &

INTERVAL=5  # segundos entre cada snapshot
SESSION_KEY="${1:-main}"  # session key del usuario

echo "🎧 LeadScout-Browser iniciado - Escuchando cada ${INTERVAL}s"
echo "Presiona Ctrl+C para detener"

while true; do
    # Llamar al gateway para hacer snapshot y procesar
    curl -s -X POST "http://127.0.0.1:18791/api/v1/browser/snapshot" \
        -H "Content-Type: application/json" \
        -d '{"profile": "chrome", "maxChars": 50000}' | \
        python3 -c "
import sys
import json
data = json.load(sys.stdin)
# Guardar para análisis
with open('/tmp/last_snapshot.json', 'w') as f:
    json.dump(data, f)
print('Snapshot capturado')
"
    
    sleep $INTERVAL
done
