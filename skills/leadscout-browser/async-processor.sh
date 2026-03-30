#!/bin/bash
# Async Processor - Consume cola de snapshots y procesa leads
# Corre continuo en background, sin presión de tiempo

QUEUE_DIR="/workspace/skills/leadscout-browser/queue"
PROCESSED_DIR="/workspace/skills/leadscout-browser/processed"
LOG_FILE="/tmp/async-processor.log"

mkdir -p "$PROCESSED_DIR"

echo "[$(date)] 🔄 Async Processor iniciado - Consumiendo cola..." | tee -a $LOG_FILE

while true; do
    # Buscar snapshots pendientes
    SNAPSHOTS=($QUEUE_DIR/snapshot_*.json)
    
    if [ -f "${SNAPSHOTS[0]}" ]; then
        for snapshot in "${SNAPSHOTS[@]}"; do
            if [ -f "$snapshot" ]; then
                FILENAME=$(basename "$snapshot")
                echo "[$(date)] 🔍 Procesando $FILENAME..." | tee -a $LOG_FILE
                
                # Analizar leads (sin guardar aún)
                python3 /workspace/skills/leadscout-browser/analyze_leads.py "$snapshot" >> $LOG_FILE 2>&1
                
                # Si hay leads detectados, guardarlos
                if [ -f "/tmp/detected_leads.json" ]; then
                    LEAD_COUNT=$(jq '. | length' /tmp/detected_leads.json)
                    if [ "$LEAD_COUNT" -gt 0 ]; then
                        echo "[$(date)] 💾 Guardando $LEAD_COUNT leads en Notion..." | tee -a $LOG_FILE
                        python3 /workspace/skills/leadscout-browser/lead_processor.py >> $LOG_FILE 2>&1
                    fi
                    rm -f /tmp/detected_leads.json
                fi
                
                # Mover a procesados
                mv "$snapshot" "$PROCESSED_DIR/$FILENAME"
                echo "[$(date)] ✅ $FILENAME completado" | tee -a $LOG_FILE
                
                # Pausa para no saturar APIs
                sleep 3
            fi
        done
    else
        # No hay nada en cola, dormir
        sleep 5
    fi
done
