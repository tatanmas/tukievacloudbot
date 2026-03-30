#!/usr/bin/env python3
"""
Web search sin APIs - usando técnicas básicas de scraping
Prioridad: WhatsApp > Email > Web > Nombre
"""
import http.client
import json
import re
import ssl
from urllib.parse import quote, urlparse

class SimpleWebSearcher:
    """Buscador web básico sin APIs externas."""
    
    def __init__(self):
        self.results_cache = {}
    
    def search_duckduckgo(self, query, max_results=10):
        """Buscar en DuckDuckGo (más permisivo que Google)."""
        try:
            conn = http.client.HTTPSConnection("html.duckduckgo.com")
            encoded = quote(query)
            path = f"/html/?q={encoded}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            
            conn.request("GET", path, headers=headers)
            resp = conn.getresponse()
            html = resp.read().decode('utf-8', errors='ignore')
            conn.close()
            
            # Extraer resultados básicos
            results = []
            # Patrones simples para extraer títulos y URLs
            title_pattern = re.findall(r'<a[^>]+class="result__a"[^>]*>([^<]+)</a>', html)
            url_pattern = re.findall(r'href="(https?://[^"]+)"', html)
            
            for i, title in enumerate(title_pattern[:max_results]):
                url = url_pattern[i] if i < len(url_pattern) else ""
                results.append({
                    "title": title.strip(),
                    "url": url,
                    "source": "duckduckgo"
                })
            
            return results
        except Exception as e:
            return [{"error": str(e)}]
    
    def extract_contact_from_page(self, url):
        """Extraer teléfono, email y WhatsApp de una página web."""
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return None
            
            conn = http.client.HTTPSConnection(parsed.netloc, timeout=10)
            path = parsed.path if parsed.path else "/"
            if parsed.query:
                path += "?" + parsed.query
            
            headers = {"User-Agent": "Mozilla/5.0 (compatible; TukiBot/1.0)"}
            conn.request("GET", path, headers=headers)
            resp = conn.getresponse()
            html = resp.read().decode('utf-8', errors='ignore')
            conn.close()
            
            contacts = {
                "phones": [],
                "emails": [],
                "whatsapp": [],
                "instagram": [],
                "web": url
            }
            
            # Teléfonos Chile (+56 9 XXXX XXXX)
            phone_patterns = [
                r'(?:whatsapp|wa\.me)[^\d]*(\+?56\s*9\s*\d[\s\-\d]*)',
                r'(\+?56\s*9\s*\d[\s\-\d]{6,})',
                r'tel[:\s]*(\+?56[\s\-\d]+)',
            ]
            for pattern in phone_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                contacts["phones"].extend([self.clean_phone(m) for m in matches if m])
            
            # Emails
            email_pattern = r'[\w.+-]+@[\w.-]+\.[\w]{2,}'
            emails = re.findall(email_pattern, html)
            contacts["emails"] = [e for e in emails if 'example' not in e and 'domain' not in e]
            
            # WhatsApp links
            wa_pattern = r'(?:wa\.me|whatsapp\.com)[^"\s]*'
            wa_matches = re.findall(wa_pattern, html)
            contacts["whatsapp"] = list(set(wa_matches))
            
            # Instagram
            ig_pattern = r'instagram\.com/([\w.]+)'
            ig_matches = re.findall(ig_pattern, html)
            if ig_matches:
                contacts["instagram"] = [f"@{m}" for m in ig_matches]
            
            # Limpiar duplicados
            contacts["phones"] = list(set(contacts["phones"]))[:3]
            contacts["emails"] = list(set(contacts["emails"]))[:2]
            
            return contacts
        except Exception as e:
            return {"error": str(e), "web": url}
    
    def clean_phone(self, phone):
        """Limpiar y normalizar número telefónico."""
        cleaned = re.sub(r'[^\d+]', '', phone)
        # Convertir a formato internacional
        if cleaned.startswith('569') or cleaned.startswith('56'):
            return cleaned
        elif cleaned.startswith('9') and len(cleaned) == 9:
            return f"+56{cleaned}"
        return cleaned
    
    def search_hotels_santiago(self):
        """Búsqueda específica para hoteles en Santiago."""
        queries = [
            "hoteles boutique santiago chile contacto whatsapp",
            "hostales santiago chile instagram whatsapp",
            "alojamiento providencia santiago telefono",
            "hotel lastarria santiago contacto",
            "hostal backpacking santiago chile",
            "cabanas santiago chile contacto",
            "coliving santiago chile",
        ]
        
        all_results = []
        for query in queries[:3]:  # Limitar para no saturar
            results = self.search_duckduckgo(query, max_results=5)
            for r in results:
                if 'error' not in r:
                    contacts = self.extract_contact_from_page(r['url'])
                    r['contacts'] = contacts
            all_results.extend(results)
        
        return all_results

if __name__ == "__main__":
    searcher = SimpleWebSearcher()
    print("🔍 Buscando hoteles en Santiago...")
    results = searcher.search_hotels_santiago()
    print(f"\nEncontrados {len(results)} resultados:")
    for r in results[:5]:
        print(f"\n📍 {r.get('title', 'N/A')}")
        print(f"   URL: {r.get('url', 'N/A')[:60]}...")
        if 'contacts' in r and 'error' not in r['contacts']:
            c = r['contacts']
            if c['whatsapp']:
                print(f"   📱 WhatsApp: {c['whatsapp'][0]}")
            elif c['phones']:
                print(f"   ☎️ Tel: {c['phones'][0]}")
            if c['emails']:
                print(f"   ✉️ Email: {c['emails'][0]}")
