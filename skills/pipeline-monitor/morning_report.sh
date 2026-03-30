#!/bin/bash
# Morning Report - Alerta diaria de pipeline
# Ejecutar a las 9am todos los días

REPORT_FILE="/tmp/pipeline_report_$(date +%Y%m%d).txt"

echo "📊 PIPELINE REPORT - $(date '+%A %d %B %Y %H:%M')" > $REPORT_FILE
echo "═══════════════════════════════════════════════
" >> $REPORT_FILE

# Ejecutar check de estancados
./check_stalled.sh >> $REPORT_FILE 2>&1

# Estadísticas rápidas
echo "" >> $REPORT_FILE
echo "📈 ACCIONES SUGERIDAS HOY:" >> $REPORT_FILE
echo "   1. Contactar leads en estado 'Contactar'
   2. Enriquecer leads 'Esperando información'
   3. Revisar leads >7 días esperando respuesta
   4. Actualizar notas de seguimiento
" >> $REPORT_FILE

# Mostrar reporte
cat $REPORT_FILE

# Opcional: enviar por Slack/WhatsApp (configurar webhook)
# curl -X POST slack_webhook -d @s$REPORT_FILE
echo ""
echo "✅ Reporte guardado en: $REPORT_FILE"
