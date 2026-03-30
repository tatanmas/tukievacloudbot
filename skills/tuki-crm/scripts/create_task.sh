#!/bin/bash
# Create a task in Eva's Notion task database
set -e

NOTION_TOKEN="${NOTION_TOKEN}"
TASKS_DB_ID="0fc9eb3f-e52b-43ae-8bd1-8cd0c700184a"

TITLE="$1"
CONTEXT="${2:-Backlog Eva}"
STATUS="${3:-Pendiente}"
NOTES="${4:-}"

if [ -z "$NOTION_TOKEN" ]; then
    echo "Error: NOTION_TOKEN not set"
    exit 1
fi

DATE=$(date -u +%Y-%m-%d)

JSON_PAYLOAD=$(cat <<EOF
{
    "parent": {"database_id": "$TASKS_DB_ID"},
    "properties": {
        "Título": {"title": [{"text": {"content": "$TITLE"}}]},
        "Estado": {"status": {"name": "$STATUS"}},
        "Contexto": {"multi_select": [{"name": "$CONTEXT"}]},
        "Fecha": {"date": {"start": "$DATE"}}
EOF
)

if [ -n "$NOTES" ]; then
    JSON_PAYLOAD+=$(cat <<EOF
,
        "Notas": {"rich_text": [{"text": {"content": "$NOTES"}}]}
EOF
)
fi

JSON_PAYLOAD+="}}"

curl -s -X POST https://api.notion.com/v1/pages \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: 2022-06-28" \
    -d "$JSON_PAYLOAD" | jq -r '.id'
