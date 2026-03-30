#!/usr/bin/env python3
"""
LeadScout Browser Analyzer
Analiza snapshots del navegador y extrae leads automáticamente
"""
import json
import re
import sys
from typing import List, Dict, Optional

class LeadAnalyzer:
    def __init__(self):
        self.leads_found = []
        
    def analyze(self, snapshot_data: dict) -> List[Dict]:
        """Analiza snapshot y extrae leads"""
        leads = []
        
        # Buscar hoteles en Google Maps
        hotels = self._extract_hotels_from_maps(snapshot_data)
        leads.extend(hotels)
        
        # Buscar hostales
        hostels = self._extract_hostels(snapshot_data)
        leads.extend(hostels)
        
        # Buscar experiencias/tours
        experiences = self._extract_experiences(snapshot_data)
        leads.extend(experiences)
        
        return leads
    
    def _extract_hotels_from_maps(self, data: dict) -> List[Dict]:
        """Extrae hoteles de Google Maps"""
        hotels = []
        snapshot_text = json.dumps(data)
        
        # Patrones de Google Maps para hoteles
        hotel_patterns = [
            r'"([^"]+Hotel[^"]*)".*?"(\d+,?\d*)\s*estrellas"',
            r'hotel.*?"([^"]+)".*?"(\d+[\.,]?\d*)\s*estrellas"',
        ]
        
        # Buscar hoteles con rating
        if 'estrellas' in snapshot_text.lower():
            # Extraer bloques que parecen hoteles
            for ref, item in data.items():
                if isinstance(item, dict):
                    text = json.dumps(item).lower()
                    if any(kw in text for kw in ['hotel', 'hospedaje']):
                        hotel = self._parse_hotel_item(item)
                        if hotel and hotel.get('nombre'):
                            hotels.append(hotel)
        
        return hotels
    
    def _parse_hotel_item(self, item: dict) -> Optional[Dict]:
        """Parsea un item de hotel"""
        text = json.dumps(item)
        
        # Extraer nombre
        nombre = self._extract_field(item, ['name', 'nombre', 'title'])
        
        # Extraer rating
        rating = self._extract_rating(text)
        
        # Extraer precio
        precio = self._extract_price(text)
        
        # Clasificar tipo
        tipo = self._classify_type(text, nombre)
        
        if nombre and self._is_valid_lead(nombre):
            return {
                'nombre': nombre,
                'tipo': tipo,
                'rating': rating,
                'precio': precio,
                'fuente': 'Google Maps',
                'url': self._extract_url(item),
                'telefono': self._extract_phone(text),
                'raw_data': item
            }
        return None
    
    def _extract_hostels(self, data: dict) -> List[Dict]:
        """Extrae hostales"""
        hostels = []
        # Similar a hoteles pero buscando "hostal", "hostel"
        return hostels
    
    def _extract_experiences(self, data: dict) -> List[Dict]:
        """Extrae experiencias/tours"""
        experiences = []
        # Buscar tours, excursiones, etc.
        return experiences
    
    def _extract_field(self, item: dict, field_names: list) -> Optional[str]:
        """Extrae campo de cualquiera de los nombres posibles"""
        for field in field_names:
            if field in item:
                val = item[field]
                if isinstance(val, str):
                    return val
                elif isinstance(val, list) and val:
                    return str(val[0])
        return None
    
    def _extract_rating(self, text: str) -> Optional[str]:
        """Extrae rating del texto"""
        patterns = [
            r'(\d+[\.,]?\d*)\s*estrellas',
            r'rating[\s:]+(\d+[\.,]?\d*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_price(self, text: str) -> Optional[str]:
        """Extrae precio del texto"""
        # Buscar patrones como $45,9 k, $110.000, etc.
        patterns = [
            r'\$([\d.,]+)\s*k?',
            r'\$\s*([\d.,]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return '$' + match.group(1)
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extrae teléfono"""
        pattern = r'\(\s*(\d+)\s*\)\s*(\d[\d\s]*)'
        match = re.search(pattern, text)
        if match:
            return f"+56{match.group(1)}{match.group(2).replace(' ', '')}"
        return None
    
    def _extract_url(self, item: dict) -> Optional[str]:
        """Extrae URL"""
        if 'url' in item:
            return item['url']
        return None
    
    def _classify_type(self, text: str, nombre: str) -> str:
        """Clasifica el tipo de lead"""
        text_lower = text.lower()
        nombre_lower = (nombre or '').lower()
        
        if any(kw in text_lower + nombre_lower for kw in ['hotel', 'alojamiento', 'hospedaje']):
            return 'Hotel'
        elif any(kw in text_lower + nombre_lower for kw in ['hostal', 'hostel', 'pensión']):
            return 'Hostal'
        elif any(kw in text_lower + nombre_lower for kw in ['tour', 'excursión', 'experiencia', 'aventura']):
            return 'Experiencias'
        return 'Otro'
    
    def _is_valid_lead(self, nombre: str) -> bool:
        """Verifica si es un lead válido"""
        if not nombre or len(nombre) < 3:
            return False
        # Evitar falsos positivos
        invalid = ['google', 'maps', 'search', 'com', 'http', 'menu', 'cerrar']
        return nombre.lower() not in invalid


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Uso: python3 analyze_leads.py <snapshot.json>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    analyzer = LeadAnalyzer()
    leads = analyzer.analyze(data)
    
    print(f"📊 Leads encontrados: {len(leads)}")
    for i, lead in enumerate(leads, 1):
        print(f"\n{i}. {lead['nombre']}")
        print(f"   Tipo: {lead['tipo']}")
        print(f"   Rating: {lead.get('rating', 'N/A')}")
        print(f"   Precio: {lead.get('precio', 'N/A')}")
        if lead.get('telefono'):
            print(f"   Tel: {lead['telefono']}")
    
    # Guardar leads para procesamiento
    with open('/tmp/detected_leads.json', 'w') as f:
        json.dump(leads, f, indent=2)
    
    return leads

if __name__ == '__main__':
    main()
