#!/usr/bin/env python3
"""
Script para crear un nuevo lead en la base de Tuki en Notion.
Uso: python3 create_lead.py --nombre "Nombre" [--telefono TEL] [--email EMAIL]
                          [--web URL] [--pais PAIS] [--lugar LUGAR] [--tipo TIPO]
                          [--fuente FUENTE] [--interes INTERES] [--valor N]
                          [--estado ESTADO] [--notas NOTAS] [--responsable RESP]
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
import os

DATABASE_ID = "303ddd5f-c230-81a3-a2d4-000be9d8a045"
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

def parse_multi(value):
    """Parsea un valor multiselect (separado por comas)."""
    if not value:
        return []
    return [{"name": v.strip()} for v in value.split(",")]

def main():
    parser = argparse.ArgumentParser(description="Crear lead en Tuki")
    parser.add_argument("--nombre", required=True, help="Nombre del lead")
    parser.add_argument("--telefono", help="Teléfono de contacto")
    parser.add_argument("--email", help="Email")
    parser.add_argument("--web", help="Sitio web")
    parser.add_argument("--maps", help="URL de Google Maps")
    parser.add_argument("--pais", help="País(es) separados por coma")
    parser.add_argument("--lugar", help="Lugar(es) separados por coma")
    parser.add_argument("--tipo", help="Tipo de cliente (Experiencias, Hostal, Hotel)")
    parser.add_argument("--fuente", help="Fuente del lead")
    parser.add_argument("--interes", default="Medio", help="Interés (Alto, Medio, Bajo)")
    parser.add_argument("--valor", type=float, help="Valor potencial")
    parser.add_argument("--estado", default="Nuevo", help="Estado inicial")
    parser.add_argument("--notas", help="Notas del lead")
    parser.add_argument("--responsable", help="Responsable")
    parser.add_argument("--fecha-contacto", help="Fecha de contacto (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN no configurado", file=sys.stderr)
        sys.exit(1)
    
    properties = {
        "Nombre del Leadp": {
            "title": [{"text": {"content": args.nombre}}]
        },
        "Estado": {
            "status": {"name": args.estado}
        },
        "Interés": {
            "select": {"name": args.interes}
        }
    }
    
    if args.telefono:
        properties["Teléfono de Contacto"] = {"phone_number": args.telefono}
    
    if args.email:
        properties["Email"] = {"email": args.email}
    
    if args.web:
        properties["Web"] = {"url": args.web}
    
    if args.maps:
        properties["Google maps"] = {"url": args.maps}
    
    if args.pais:
        properties["País"] = {"multi_select": parse_multi(args.pais)}
    
    if args.lugar:
        properties["Lugar"] = {"multi_select": parse_multi(args.lugar)}
    
    if args.tipo:
        properties["Tipo de cliente"] = {"multi_select": parse_multi(args.tipo)}
    
    if args.fuente:
        properties["Fuente de Lead"] = {"select": {"name": args.fuente}}
    
    if args.valor:
        properties["Valor Potencial"] = {"number": args.valor}
    
    if args.fecha_contacto:
        properties["Fecha de Contacto"] = {"date": {"start": args.fecha_contacto}}
    
    if args.notas:
        properties["Notas"] = {"rich_text": [{"text": {"content": args.notas}}]}
    
    if args.responsable:
        properties["Responsable"] = {"rich_text": [{"text": {"content": args.responsable}}]}
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    result = notion_api("POST", "/pages", data)
    
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    print(json.dumps({
        "success": True,
        "id": result.get("id"),
        "url": result.get("url"),
        "nombre": args.nombre
    }, indent=2))

if __name__ == "__main__":
    main()
