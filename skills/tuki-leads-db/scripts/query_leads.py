#!/usr/bin/env python3
"""
Script para consultar leads de la base de Tuki en Notion.
Uso: python3 query_leads.py [--estado ESTADO] [--pais PAIS] [--lugar LUGAR]
                          [--tipo TIPO] [--interes INTERES] [--fuente FUENTE]
                          [--responsable RESPONSABLE] [--limit N]
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

def build_filter(args):
    """Construye el filtro para la query de Notion."""
    filters = []
    
    if args.estado:
        filters.append({
            "property": "Estado",
            "status": {"equals": args.estado}
        })
    
    if args.pais:
        filters.append({
            "property": "País",
            "multi_select": {"contains": args.pais}
        })
    
    if args.lugar:
        filters.append({
            "property": "Lugar",
            "multi_select": {"contains": args.lugar}
        })
    
    if args.tipo:
        filters.append({
            "property": "Tipo de cliente",
            "multi_select": {"contains": args.tipo}
        })
    
    if args.interes:
        filters.append({
            "property": "Interés",
            "select": {"equals": args.interes}
        })
    
    if args.fuente:
        filters.append({
            "property": "Fuente de Lead",
            "select": {"equals": args.fuente}
        })
    
    if args.responsable:
        filters.append({
            "property": "Responsable",
            "rich_text": {"contains": args.responsable}
        })
    
    if len(filters) == 0:
        return {}
    elif len(filters) == 1:
        return filters[0]
    else:
        return {"and": filters}

def format_lead(result):
    """Formatea un lead para mostrarlo."""
    p = result.get("properties", {})
    
    name = p.get("Nombre del Leadp", {}).get("title", [{}])[0].get("text", {}).get("content", "Sin nombre")
    estado = p.get("Estado", {}).get("status", {}).get("name", "")
    telefono = p.get("Teléfono de Contacto", {}).get("phone_number", "")
    email = p.get("Email", {}).get("email", "")
    web = p.get("Web", {}).get("url", "")
    
    paises = [opt.get("name") for opt in p.get("País", {}).get("multi_select", [])]
    lugares = [opt.get("name") for opt in p.get("Lugar", {}).get("multi_select", [])]
    tipos = [opt.get("name") for opt in p.get("Tipo de cliente", {}).get("multi_select", [])]
    
    fuente = p.get("Fuente de Lead", {}).get("select", {}).get("name", "")
    interes = p.get("Interés", {}).get("select", {}).get("name", "")
    valor = p.get("Valor Potencial", {}).get("number")
    
    fecha_contacto = p.get("Fecha de Contacto", {}).get("date", {}).get("start", "")
    fecha_seguimiento = p.get("Fecha Próximo Seguimiento", {}).get("date", {}).get("start", "")
    
    responsable = "".join([t.get("text", {}).get("content", "") 
                          for t in p.get("Responsable", {}).get("rich_text", [])])
    
    return {
        "id": result.get("id"),
        "nombre": name,
        "estado": estado,
        "telefono": telefono,
        "email": email,
        "web": web,
        "paises": paises,
        "lugares": lugares,
        "tipos": tipos,
        "fuente": fuente,
        "interes": interes,
        "valor_potencial": valor,
        "fecha_contacto": fecha_contacto,
        "fecha_seguimiento": fecha_seguimiento,
        "responsable": responsable
    }

def main():
    parser = argparse.ArgumentParser(description="Consultar leads de Tuki en Notion")
    parser.add_argument("--estado", help="Filtrar por estado (Contactar, Nuevo, Esperando respuesta, etc.)")
    parser.add_argument("--pais", help="Filtrar por país")
    parser.add_argument("--lugar", help="Filtrar por lugar (Viña del mar, Uyuni, Pucón, etc.)")
    parser.add_argument("--tipo", help="Filtrar por tipo de cliente (Experiencias, Hostal, Hotel)")
    parser.add_argument("--interes", help="Filtrar por interés (Alto, Medio, Bajo)")
    parser.add_argument("--fuente", help="Filtrar por fuente de lead")
    parser.add_argument("--responsable", help="Filtrar por responsable")
    parser.add_argument("--limit", type=int, default=100, help="Límite de resultados")
    
    args = parser.parse_args()
    
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN no configurado", file=sys.stderr)
        sys.exit(1)
    
    filter_body = build_filter(args)
    
    query_body = {"page_size": args.limit}
    if filter_body:
        query_body["filter"] = filter_body
    
    # Nota: en Notion API v2025-09-03, para query se usa database_id
    result = notion_api("POST", f"/databases/{DATABASE_ID}/query", query_body)
    
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    leads = [format_lead(r) for r in result.get("results", [])]
    print(json.dumps(leads, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
