#!/usr/bin/env python3
"""Create tasks/notes in Notion using http.client (no external deps)."""
import os
import sys
import json
import http.client
from datetime import datetime

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")

# IDs correctos de las URLs proporcionadas por Tatan
TASKS_DB = "9b6a3ee2-05ab-4e47-bc13-a401de09a900"  # tareas
NOTES_DB = "edfeb377-32fd-4636-bf68-bf6252a04c64"  # notas  
LEADS_DB = "303ddd5f-c230-8087-9f4b-f6f51c7f5ded"  # leads de captacion

def notion_request(method, path, body=None):
    conn = http.client.HTTPSConnection("api.notion.com")
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    conn.request(method, path, json.dumps(body) if body else None, headers)
    resp = conn.getresponse()
    data = resp.read().decode()
    conn.close()
    return json.loads(data)

def create_task(title, context="Eva", status="🍵"):
    """Create a task in the tasks database."""
    props = {
        "Task name": {"title": [{"text": {"content": title}}]},
        "Estado": {"status": {"name": status}},
        "Contexto": {"multi_select": [{"name": context}]},
        "Fecha de ejecución": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
    }
    
    return notion_request("POST", "/v1/pages", {
        "parent": {"database_id": TASKS_DB},
        "properties": props
    })

def create_note(title, content, tipo="Eva"):
    """Create a note in the notes database."""
    props = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Tipo": {"multi_select": [{"name": tipo}]}
    }
    # Notas no tiene campo de contenido directo, se puede agregar en el cuerpo de la página
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content[:1800]}}]
            }
        }
    ]
    return notion_request("POST", "/v1/pages", {
        "parent": {"database_id": NOTES_DB},
        "properties": props,
        "children": children
    })

def query_leads(filter_props=None, limit=10):
    """Query leads from the leads database."""
    body = {"page_size": limit}
    if filter_props:
        body["filter"] = filter_props
    return notion_request("POST", f"/v1/databases/{LEADS_DB}/query", body)

def query_tasks(filter_props=None, limit=10):
    """Query tasks from the tasks database."""
    body = {"page_size": limit}
    if filter_props:
        body["filter"] = filter_props
    return notion_request("POST", f"/v1/databases/{TASKS_DB}/query", body)

def query_notes(filter_props=None, limit=10):
    """Query notes from the notes database."""
    body = {"page_size": limit}
    if filter_props:
        body["filter"] = filter_props
    return notion_request("POST", f"/v1/databases/{NOTES_DB}/query", body)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["task", "note", "query_leads", "query_tasks", "query_notes"])
    parser.add_argument("--title", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--context", default="Eva")
    parser.add_argument("--status", default="Pendiente")
    parser.add_argument("--tipo", default="Eva")
    args = parser.parse_args()
    
    if args.action == "task":
        result = create_task(args.title, args.context, args.status)
    elif args.action == "note":
        result = create_note(args.title, args.content, args.tipo)
    elif args.action == "query_leads":
        result = query_leads(limit=5)
    elif args.action == "query_tasks":
        result = query_tasks(limit=5)
    elif args.action == "query_notes":
        result = query_notes(limit=5)
    
    print(json.dumps(result, indent=2))
