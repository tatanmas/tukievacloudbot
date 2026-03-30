#!/usr/bin/env python3
"""
LeadProcessor - Guarda leads detectados en Notion
Recibe leads del analyzer y los persiste en la base de datos
"""
import json
import os
import requests
from typing import Dict, List

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = "303ddd5f-c230-8087-9f4b-f6f51c7f5ded"

class LeadProcessor:
    def __init__(self):
        self.notion_token = NOTION_TOKEN
        self.database_id = DATABASE_ID
        self.api_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def process_leads(self, leads: List[Dict]):
        """Procesa y guarda una lista de leads"""
        print(f"🔄 Procesando {len(leads)} leads...")
        
        for lead in leads:
            # Verificar si ya existe (por nombre)
            if self._lead_exists(lead['nombre']):
                print(f"  ⚠️  Ya existe: {lead['nombre'][:50]}...")
                continue
            
            # Guardar en Notion
            success = self._save_to_notion(lead)
            if success:
                print(f"  ✅ Guardado: {lead['nombre'][:50]}")
            else:
                print(f"  ❌ Error guardando: {lead['nombre'][:50]}")
    
    def _lead_exists(self, nombre: str) -> bool:
        """Verifica si ya existe un lead con ese nombre"""
        # Query a Notion
        url = f"{self.api_url}/databases/{self.database_id}/query"
        payload = {
            "filter": {
                "property": "Nombre del Leapd",
                "title": {
                    "equals": nombre
                }
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                return len(data.get('results', [])) > 0
        except Exception as e:
            print(f"Error verificando existencia: {e}")
        
        return False
    
    def _save_to_notion(self, lead: Dict) -> bool:
        """Guarda un lead en Notion"""
        url = f"{self.api_url}/pages"
        
        # Construir notas
        notas = f"Rating: {lead.get('rating', 'N/A')}\n"
        notas += f"Precio: {lead.get('precio', 'N/A')}\n"
        if lead.get('servicios'):
            notas += f"Servicios: {', '.join(lead['servicios'])}\n"
        if lead.get('direccion'):
            notas += f"Dirección: {lead['direccion']}\n"
        
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Nombre del Leapd": {
                    "title": [{"text": {"content": lead['nombre'][:100]}}]
                },
                "Tipo de cliente": {
                    "multi_select": [{"name": lead.get('tipo', 'Hotel')}]
                },
                "Estado": {
                    "status": {"name": "Nuevo"}
                },
                "Fuente de Lead": {
                    "select": {"name": "Google Maps"}
                },
                "País": {
                    "multi_select": [{"name": "Chile"}]
                },
                "Notas": {
                    "rich_text": [{"text": {"content": notas}}]
                }
            }
        }
        
        # Añadir campos opcionales si existen
        if lead.get('telefono'):
            payload["properties"]["Teléfono de Contacto"] = {
                "phone_number": lead['telefono']
            }
        
        if lead.get('url'):
            payload["properties"]["Web"] = {"url": lead['url']}
        
        if lead.get('google_maps_url'):
            payload["properties"]["Google maps"] = {"url": lead['google_maps_url']}
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error guardando en Notion: {e}")
            return False


def main():
    """Procesa leads desde archivo JSON"""
    leads_file = '/tmp/detected_leads.json'
    
    if not os.path.exists(leads_file):
        print("No hay leads pendientes para procesar")
        return
    
    with open(leads_file, 'r') as f:
        leads = json.load(f)
    
    processor = LeadProcessor()
    processor.process_leads(leads)
    
    # Limpiar archivo procesado
    os.remove(leads_file)
    print("\n✅ Procesamiento completado")


if __name__ == '__main__':
    main()
