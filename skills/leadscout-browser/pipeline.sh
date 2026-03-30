#!/bin/bash
# LeadScout Browser - Pipeline Completo 24/7
# Este script se ejecuta cada 5-10 segundos via cron

LOG_FILE="/tmp/leadscout-browser.log"
SNAPSHOT_FILE="/tmp/last_snapshot.json"

echo "[$(date)] 🎧 Iniciando ciclo de captura..." >> $LOG_FILE

# 1. Tomar snapshot del navegador (reemplazar con curl al gateway si es necesario)
# Nota: Esto requiere que el navegador esté adjunto

# 2. Si hay snapshot disponible, analizarlo
if [ -f "$SNAPSHOT_FILE" ]; then
    echo "[$(date)] 🔍 Analizando leads..." >> $LOG_FILE
    
    # Analizar leads
    python3 /workspace/skills/leadscout-browser/analyze_leads.py "$SNAPSHOT_FILE" >> $LOG_FILE 2>&1
    
    # Si se detectaron leads, procesarlos
    if [ -f "/tmp/detected_leads.json" ]; then
        echo "[$(date)] 💾 Guardando leads en Notion..." >> $LOG_FILE
        python3 /workspace/skills/leadscout-browser/lead_processor.py >> $LOG_FILE 2>&1
    fi
fi

echo "[$(date)] ✅ Ciclo completado" >> $LOG_FILE
