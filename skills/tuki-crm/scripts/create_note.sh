#!/bin/bash
# Create a note in Eva's Notion notes database
set -e

NOTION_TOKEN="${NOTION_TOKEN}"
NOTES_DB_ID="2c35f7bc-e9cb-482d-820f-b7a07799ba03"

TITLE="$1"
CONTENT="$2"
CONTEXT="${3:-Eva}"

if [ -z "$NOTION_TOKEN" ]; then
    echo "Error: NOTION_TOKEN not set"
    exit 1
fi

DATE=$(date -u +%Y-%m-%d)

# Truncate content to avoid errors
CONTENT_SHORT="${CONTENT:0:1800}"

curl -s -X POST https://api.notion.com/v1/pages \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: 2022-06-28" \
    -d "{
        \"parent\": {\"database_id\": \"$NOTES_DB_ID\"},
        \"properties\": {
            \"Título\": {\"title\": [{\"text\": {\"content\": \"$TITLE\"}}]},
            \"Fecha\": {\"date\": {\"start\": \"$DATE\"}},
            \"Contexto\": {\"multi_select\": [{\"name\": \"$CONTEXT\"}]},
            \"Contenido\": {\"rich_text\": [{\"text\": {\"content\": \"$CONTENT_SHORT\"}}]}
        }
    }" | jq -r '.id'
