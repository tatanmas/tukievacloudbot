#!/usr/bin/env python3
"""Create a note in Eva's Notion notes database."""
import os
import sys
import json
import argparse
from datetime import datetime

import requests

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTES_DB_ID = "2c35f7bc-e9cb-482d-820f-b7a07799ba03"

def create_note(title, content, context="Eva", tags=None):
    """Create a note in Notion."""
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set")
        sys.exit(1)
    
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    properties = {
        "Título": {"title": [{"text": {"content": title}}]},
        "Fecha": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "Contexto": {"multi_select": [{"name": context}]},
        "Contenido": {"rich_text": [{"text": {"content": content[:2000]}}]}
    }
    
    if tags:
        properties["Tags"] = {"multi_select": [{"name": t} for t in tags]}
    
    payload = {
        "parent": {"database_id": NOTES_DB_ID},
        "properties": properties
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Note created: {data.get('id')}")
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--context", default="Eva")
    parser.add_argument("--tags", nargs="+")
    args = parser.parse_args()
    
    create_note(args.title, args.content, args.context, args.tags)
