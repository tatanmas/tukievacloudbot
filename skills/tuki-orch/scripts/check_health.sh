#!/bin/bash
# Health check de todos los agentes Tuki

LOG_FILE="/workspace/logs/health.log"
mkdir -p /workspace/logs

echo "=== Health Check $(date) ===" >> $LOG_FILE

# Agentes esperados
AGENTS=(
  "CRMKeeper:78f28d72-1716-4361-bd46-dd5d1400a4c3"
  "LeadScout:fd1c1a22-84af-4ca6-abb1-777126db11a9"
  "SalesCloser:2d3792a0-1de8-427a-b286-c27318c76935"
)

for agent in "${AGENTS[@]}"; do
  IFS=':' read -r name session_key <<< "$agent"
  
  # Verificar si el session existe revisando logs recientes
  if grep -q "$session_key" /workspace/.clawdbot/sessions/*.jsonl 2>/dev/null | head -1; then
    echo "✓ $name: Activo" >> $LOG_FILE
  else
    echo "✗ $name: INACTIVO - Necesita reactivación" >> $LOG_FILE
    echo "  SessionKey: $session_key" >> $LOG_FILE
  fi
done

echo "" >> $LOG_FILE
cat $LOG_FILE | tail -20
