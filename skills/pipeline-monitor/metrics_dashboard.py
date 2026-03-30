#!/usr/bin/env python3
"""
Pipeline Metrics Dashboard - Calcula estadísticas de flujo
Ejecutar: python3 metrics_dashboard.py
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = "303ddd5f-c230-8087-9f4b-f6f51c7f5ded"

def calculate_metrics(leads):
    """Calcula métricas del pipeline"""
    
    metrics = {
        "total_leads": len(leads),
        "by_status": defaultdict(int),
        "avg_time_per_status": defaultdict(list),
        "conversion_rates": {},
        "stalled": {
            "critica": 0,
            "media": 0,
            "seguimiento": 0
        },
        "leads_this_week": 0,
        "leads_today": 0
    }
    
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    
    for lead in leads:
        props = lead.get('properties', {})
        estado = props.get('Estado', {}).get('status', {}).get('name', 'Desconocido')
        creado = lead.get('created_time', '')
        ultima_ed = lead.get('last_edited_time', creado)
        
        # Contar por estado
        metrics["by_status"][estado] += 1
        
        # Detectar estancados
        try:
            fecha_edicion = datetime.fromisoformat(ultima_ed.replace('Z', '+00:00').replace('+00:00', ''))
            dias_sin_mov = (hoy - fecha_edicion).days
        except:
            dias_sin_mov = 0
        
        if estado == "Contactar" and dias_sin_mov >= 5:
            metrics["stalled"]["critica"] += 1
        elif estado == "Esperando información" and dias_sin_mov >= 3:
            metrics["stalled"]["media"] += 1
        elif estado == "Esperando respuesta" and dias_sin_mov >= 7:
            metrics["stalled"]["seguimiento"] += 1
        
        # Leads esta semana
        try:
            fecha_creacion = datetime.fromisoformat(creado.replace('Z', '+00:00').replace('+00:00', ''))
            if fecha_creacion >= hace_7_dias:
                metrics["leads_this_week"] += 1
            if fecha_creacion.date() == hoy.date():
                metrics["leads_today"] += 1
        except:
            pass
    
    return metrics


def generate_report(metrics):
    """Genera reporte de métricas"""
    
    print("━" * 50)
    print("📊 PIPELINE METRICS - TUKI")
    print("━" * 50)
    print(f"\n📈 ESTADÍSTICAS GENERALES")
    print(f"   Total leads activos: {metrics['total_leads']}")
    print(f"   Leads esta semana: {metrics['leads_this_week']}")
    print(f"   Leads hoy: {metrics['leads_today']}")
    
    print(f"\n📊 DISTRIBUCIÓN POR ESTADO")
    for estado, count in sorted(metrics["by_status"].items()):
        porcentaje = (count / metrics['total_leads']) * 100 if metrics['total_leads'] > 0 else 0
        print(f"   {estado}: {count} ({porcentaje:.1f}%)")
    
    print(f"\n🚨 LEADS ESTANCADOS")
    total_stalled = sum(metrics["stalled"].values())
    print(f"   Total: {total_stalled}")
    print(f"   - Crítica (>5 días en Contactar): {metrics['stalled']['critica']}")
    print(f"   - Media (>3 días en Esperando info): {metrics['stalled']['media']}")
    print(f"   - Seguimiento (>7 días esperando respuesta): {metrics['stalled']['seguimiento']}")
    
    # Velocidad ideal
    nuevos = metrics["by_status"].get("Nuevo", 0)
    contactar = metrics["by_status"].get("Contactar", 0)
    conversión = (contactar / nuevos * 100) if nuevos > 0 else 0
    
    print(f"\n⚡ VELOCIDAD DEL PIPELINE")
    print(f"   Conversión Nuevo→Contactar: {conversión:.1f}%")
    
    print("\n" + "━" * 50)


def save_snapshot(metrics):
    """Guarda snapshot para tendencias históricas"""
    fecha = datetime.now().strftime("%Y-%m-%d")
    archivo = f"/workspace/skills/pipeline-monitor/snapshots/{fecha}_metrics.json"
    
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    
    with open(archivo, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    print(f"\n💾 Snapshot guardado: {archivo}")


if __name__ == "__main__":
    # Simulación de datos (en producción, vienen de Notion)
    print("Nota: Este script lee de Notion en producción")
    print("Para ver métricas reales, ejecutar: ./morning_report.sh")
