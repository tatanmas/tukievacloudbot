#!/bin/bash
# LeadScout FastCapture - Solo captura, sin procesar
# Ejecuta cada 1-2 segundos, guarda snapshots en cola

QUEUE_DIR="/workspace/skills/leadscout-browser/queue"
mkdir -p "$QUEUE_DIR"

# Timestamp único
TIMESTAMP=$(date +%s%N)
SNAPSHOT_FILE="$QUEUE_DIR/snapshot_${TIMESTAMP}.json"

curl -s -X POST "http://127.0.0.1:18791/api/v1/browser/snapshot" \
    -H "Content-Type: application/json" \
    -d '{"profile": "chrome", "maxChars": 30000, "compact": true}' \
    -o "$SNAPSHOT_FILE" --max-time 3 2>/dev/null

if [ -s "$SNAPSHOT_FILE" ]; then
    echo "$(date +%H:%M:%S) 📸 Captura guardada: snapshot_${TIMESTAMP}.json"
else
    rm -f "$SNAPSHOT_FILE"
fi
