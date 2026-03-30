#!/usr/bin/env python3
"""
Script para actualizar un lead existente en la base de Tuki en Notion.
Uso: python3 update_lead.py --id PAGE_ID [--estado ESTADO] [--notas NOTAS]
                          [--fecha-seguimiento DATE] [--interes INTERES]
                          [--agregar-nota NOTA]
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
import os

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")

def notion_api(method, endpoint, data=None):
    url = f"https://api.notion.com/v1{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode('utf-8')}

def main():
    parser = argparse.ArgumentParser(description="Actualizar lead en Tuki")
    parser.add_argument("--id", required=True, help="ID de la página del lead")
    parser.add_argument("--estado", help="Nuevo estado")
    parser.add_argument("--interes", help="Nuevo nivel de interés (Alto, Medio, Bajo)")
    parser.add_argument("--notas", help="Reemplazar notas")
    parser.add_argument("--agregar-nota", help="Agregar nota al final de las existentes")
    parser.add_argument("--fecha-seguimiento", help="Fecha próximo seguimiento (YYYY-MM-DD)")
    parser.add_argument("--fecha-contacto", help="Fecha de contacto (YYYY-MM-DD)")
    parser.add_argument("--responsable", help="Responsable")
    parser.add_argument("--valor", type=float, help="Valor potencial")
    
    args = parser.parse_args()
    
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN no configurado", file=sys.stderr)
        sys.exit(1)
    
    properties = {}
    
    if args.estado:
        properties["Estado"] = {"status": {"name": args.estado}}
    
    if args.interes:
        properties["Interés"] = {"select": {"name": args.interes}}
    
    # Si estamos agregando nota, primero leemos el actual
    if args.agregar_nota:
        current = notion_api("GET", f"/pages/{args.id}")
        current_notes = ""
        if "properties" in current:
            rich_text = current["properties"].get("Notas", {}).get("rich_text", [])
            current_notes = "".join([t.get("text", {}).get("content", "") for t in rich_text])
        
        if current_notes:
            new_notes = current_notes + "\n\n" + args.agregar_nota
        else:
            new_notes = args.agregar_nota
        properties["Notas"] = {"rich_text": [{"text": {"content": new_notes}}]}
    
    if args.notas:
        properties["Notas"] = {"rich_text": [{"text": {"content": args.notas}}]}
    
    if args.fecha_seguimiento:
        properties["Fecha Próximo Seguimiento"] = {"date": {"start": args.fecha_seguimiento}}
    
    if args.fecha_contacto:
        properties["Fecha de Contacto"] = {"date": {"start": args.fecha_contacto}}
    
    if args.responsable:
        properties["Responsable"] = {"rich_text": [{"text": {"content": args.responsable}}]}
    
    if args.valor is not None:
        properties["Valor Potencial"] = {"number": args.valor}
    
    if not properties:
        print("Error: No se especificaron campos para actualizar", file=sys.stderr)
        sys.exit(1)
    
    result = notion_api("PATCH", f"/pages/{args.id}", {"properties": properties})
    
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    updates = list(properties.keys())
    print(json.dumps({
        "success": True,
        "id": args.id,
        "actualizaciones": updates
    }, indent=2))

if __name__ == "__main__":
    main()
