#!/usr/bin/env python3
"""Create a task in Eva's Notion task database."""
import os
import sys
import json
import argparse
from datetime import datetime

import requests

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
TASKS_DB_ID = "0fc9eb3f-e52b-43ae-8bd1-8cd0c700184a"

def create_task(title, database_id=None, context="Backlog Eva", status="Pendiente", notes=""):
    """Create a task in Notion."""
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set")
        sys.exit(1)
    
    db_id = database_id or TASKS_DB_ID
    
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    properties = {
        "Título": {"title": [{"text": {"content": title}}]},
        "Estado": {"status": {"name": status}},
        "Contexto": {"multi_select": [{"name": context}]},
        "Fecha": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
    }
    
    if notes:
        properties["Notas"] = {"rich_text": [{"text": {"content": notes}}]}
    
    payload = {
        "parent": {"database_id": db_id},
        "properties": properties
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Task created: {data.get('id')}")
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--database-id")
    parser.add_argument("--context", default="Backlog Eva")
    parser.add_argument("--status", default="Pendiente")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    
    create_task(args.title, args.database_id, args.context, args.status, args.notes)
