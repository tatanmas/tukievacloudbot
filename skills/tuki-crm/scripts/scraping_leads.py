#!/usr/bin/env python3
"""
Lead scraper para Tuki - Métodos de extracción de datos
"""
import http.client
import json
import os
from datetime import datetime

class LeadScraper:
    """Múltiples métodos para obtener leads de alojamientos y experiencias."""
    
    def __init__(self):
        self.notion_token = os.environ.get("NOTION_TOKEN")
        self.google_places_key = os.environ.get("GOOGLE_PLACES_API_KEY")
        
    def test_connection(self):
        """Test available data sources."""
        results = {}
        
        # Test 1: Notion API
        if self.notion_token:
            conn = http.client.HTTPSConnection("api.notion.com")
            headers = {"Authorization": f"Bearer {self.notion_token}", 
                      "Notion-Version": "2022-06-28"}
            conn.request("GET", "/v1/users/me", headers=headers)
            resp = conn.getresponse()
            results['notion'] = 'OK' if resp.status == 200 else 'FAIL'
            conn.close()
        else:
            results['notion'] = 'NO_TOKEN'
            
        # Test 2: Google Places
        if self.google_places_key:
            results['google_places'] = 'KEY_EXISTS'
        else:
            results['google_places'] = 'NO_KEY'
            
        return results
    
    def get_method_status(self):
        """Return status of all scraping methods."""
        return {
            "google_places_api": {
                "available": bool(self.google_places_key),
                "quality": "HIGH - Enriched data (name, phone, web, photos, reviews)",
                "rate_limit": "Requests per day quota",
                "cost": "Paid after free tier",
                "setup": "Add GOOGLE_PLACES_API_KEY to .env"
            },
            "brave_search_api": {
                "available": False,  # Needs BRAVE_API_KEY
                "quality": "MEDIUM - Web search results",
                "rate_limit": "1000 queries/month free",
                "cost": "Free tier available",
                "setup": "Add BRAVE_API_KEY to .env"
            },
            "manual_entry": {
                "available": True,
                "quality": "HIGH - Human verified",
                "rate_limit": "None",
                "cost": "Free",
                "setup": "Direct to notion_task.py"
            },
            "web_scraping": {
                "available": False,
                "quality": "MEDIUM - Blocked by modern sites",
                "rate_limit": "Blocked by WAF",
                "cost": "Requires proxy services",
                "setup": "Needs ScrapingBee/ScraperAPI keys"
            },
            "browser_automation": {
                "available": False,
                "quality": "HIGH - Full data",
                "rate_limit": "Resource intensive",
                "cost": "High compute",
                "setup": "Not available in this environment"
            }
        }

if __name__ == "__main__":
    scraper = LeadScraper()
    
    print("=== TEST DE CONECTIVIDAD ===")
    conn_status = scraper.test_connection()
    for source, status in conn_status.items():
        print(f"  {source}: {status}")
    
    print("\n=== MÉTODOS DE SCRAPING DISPONIBLES ===")
    methods = scraper.get_method_status()
    for method, info in methods.items():
        icon = "✅" if info["available"] else "❌"
        print(f"\n{icon} {method}")
        print(f"   Calidad: {info['quality']}")
        print(f"   Setup: {info['setup']}")
