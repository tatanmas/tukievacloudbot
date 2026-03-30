#!/bin/bash
# LeadScout Orquestador - Coordina FastCapture + AsyncProcessor

QUEUE_DIR="/workspace/skills/leadscout-browser/queue"
PROCESSED_DIR="/workspace/skills/leadscout-browser/processed"
PID_FILE="/tmp/leadscout.pid"
LOG_DIR="/workspace/skills/leadscout-browser/logs"
CAPTURE_INTERVAL=2  # segundos entre capturas

mkdir -p "$LOG_DIR"

show_status() {
    QUEUE_COUNT=$(ls -1 "$QUEUE_DIR"/snapshot_*.json 2>/dev/null | wc -l)
    PROCESSED_COUNT=$(ls -1 "$PROCESSED_DIR"/snapshot_*.json 2>/dev/null | wc -l)
    
    echo "🦄 LeadScout Browser - Estado"
    echo "═══════════════════════════════"
    echo "📸 Snapshots en cola: $QUEUE_COUNT"
    echo "✅ Procesados: $PROCESSED_COUNT"
    echo "⏱️  Intervalo captura: ${CAPTURE_INTERVAL}s"
    echo ""
    
    if [ -f "$PID_FILE" ]; then
        echo "🟢 Estado: ACTIVO"
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "   PID: $PID"
        else
            echo "   ⚠️  Proceso muerto, reiniciar"
        fi
    else
        echo "🔴 Estado: INACTIVO"
    fi
}

start_capture() {
    echo "🚀 Iniciando captura rápida (cada ${CAPTURE_INTERVAL}s)..."
    
    # Capturador rápido (background)
    (
        while true; do
            /workspace/skills/leadscout-browser/fast-capture.sh 2>&1 | tee -a "$LOG_DIR/capture.log"
            sleep $CAPTURE_INTERVAL
        done
    ) &
    CAPTURE_PID=$!
    
    # Procesador asíncrono (background)
    /workspace/skills/leadscout-browser/async-processor.sh &
    PROCESSOR_PID=$!
    
    # Guardar PIDs
    echo "$CAPTURE_PID $PROCESSOR_PID" > "$PID_FILE"
    echo "✅ Capturador PID: $CAPTURE_PID"
    echo "✅ Procesador PID: $PROCESSOR_PID"
}

stop_services() {
    if [ -f "$PID_FILE" ]; then
        read -r CAPTURE_PID PROCESSOR_PID < "$PID_FILE"
        echo "🛑 Deteniendo servicios..."
        kill "$CAPTURE_PID" 2>/dev/null && echo "   Capturador detenido"
        kill "$PROCESSOR_PID" 2>/dev/null && echo "   Procesador detenido"
        rm -f "$PID_FILE"
    else
        echo "No hay servicios activos"
    fi
}

clear_queue() {
    echo "🗑️  Limpiando cola..."
    rm -f "$QUEUE_DIR"/*.json
    echo "   $QUEUE_COUNT archivos eliminados"
}

# Menú
case "${1:-status}" in
    start)
        start_capture
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 1
        start_capture
        ;;
    status)
        show_status
        ;;
    clear)
        clear_queue
        ;;
    logs)
        tail -f "$LOG_DIR"/*.log
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|clear|logs}"
        ;;
esac
