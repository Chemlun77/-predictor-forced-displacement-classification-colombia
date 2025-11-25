"""
Script para generar mapeo entre nombres de departamentos del dataset
y nombres en el GeoJSON de Colombia
"""

import json
import requests
from difflib import get_close_matches

# Coordenadas de departamentos (del código 001)
URBAN_CENTER_COORDS = {
    'Amazonas': (-4.2153, -69.9406),
    'Antioquia': (6.2476, -75.5658),
    'Arauca': (7.0902, -70.7590),
    'Atlantico': (10.9639, -74.7964),
    'Bolivar': (10.4236, -75.5353),
    'Boyaca': (5.5353, -73.3678),
    'Caldas': (5.0703, -75.5138),
    'Caqueta': (1.6144, -75.6062),
    'Casanare': (5.3378, -72.3959),
    'Cauca': (2.4419, -76.6063),
    'Cesar': (10.4636, -73.2506),
    'Choco': (5.6947, -76.6611),
    'Cordoba': (8.7479, -75.8814),
    'Cundinamarca': (4.5981, -74.0758),
    'Guainia': (3.8653, -67.9239),
    'Guaviare': (2.5697, -72.6459),
    'Huila': (2.9273, -75.2819),
    'La Guajira': (11.5444, -72.9072),
    'Magdalena': (11.2408, -74.2099),
    'Meta': (4.1420, -73.6266),
    'Nariño': (1.2136, -77.2811),
    'Norte De Santander': (7.8939, -72.5078),
    'Putumayo': (1.1469, -76.6411),
    'Quindio': (4.5339, -75.6811),
    'Risaralda': (4.8133, -75.6961),
    'Archipielago de San Andrés, Providencia y Santa Catalina': (12.5847, -81.7006),
    'Santander': (7.1254, -73.1198),
    'Sucre': (9.3047, -75.3978),
    'Tolima': (4.4389, -75.2322),
    'Valle del Cauca': (3.4372, -76.5225),
    'Vaupes': (1.2537, -70.2369),
    'Vichada': (6.1894, -67.4936),
    'Bogota, D.C.': (4.5981, -74.0758)
}

def normalize_name(name):
    """Normaliza nombres para comparación"""
    import unicodedata
    # Remover acentos
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    # Minúsculas y espacios
    return name.lower().strip()

def download_geojson():
    """Descarga el GeoJSON de Colombia"""
    url = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_COL_1.json"
    
    print(f"Descargando GeoJSON desde: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error al descargar: {response.status_code}")
    
    print("✓ GeoJSON descargado exitosamente")
    return response.json()

def extract_department_names(geojson_data):
    """Extrae nombres de departamentos del GeoJSON"""
    names = []
    
    # Posibles campos donde puede estar el nombre
    possible_fields = ['NAME_1', 'NOMBRE_DPT', 'name', 'departamento', 'NAME']
    
    for feature in geojson_data.get('features', []):
        props = feature.get('properties', {})
        
        # Buscar el nombre en los campos posibles
        for field in possible_fields:
            if field in props:
                name = props[field]
                if name and name not in names:
                    names.append(name)
                break
    
    print(f"\n✓ {len(names)} departamentos encontrados en GeoJSON")
    print("\nDepartamentos en GeoJSON:")
    for name in sorted(names):
        print(f"  • {name}")
    
    return names

def create_mapping(dataset_names, geojson_names):
    """Crea mapeo entre nombres del dataset y GeoJSON"""
    mapping = {}
    unmatched = []
    
    print("\n" + "="*80)
    print("GENERANDO MAPEO")
    print("="*80)
    
    for dataset_name in dataset_names:
        # Normalizar para comparación
        normalized_dataset = normalize_name(dataset_name)
        
        # Buscar coincidencia exacta (normalizada)
        exact_match = None
        for geojson_name in geojson_names:
            if normalize_name(geojson_name) == normalized_dataset:
                exact_match = geojson_name
                break
        
        if exact_match:
            mapping[dataset_name] = exact_match
            print(f"✓ {dataset_name:50s} → {exact_match}")
        else:
            # Buscar coincidencias cercanas
            normalized_geojson = [normalize_name(n) for n in geojson_names]
            matches = get_close_matches(normalized_dataset, normalized_geojson, n=3, cutoff=0.6)
            
            if matches:
                # Tomar la mejor coincidencia
                best_match_idx = normalized_geojson.index(matches[0])
                best_match = geojson_names[best_match_idx]
                mapping[dataset_name] = best_match
                print(f"≈ {dataset_name:50s} → {best_match} (similar)")
            else:
                unmatched.append(dataset_name)
                mapping[dataset_name] = dataset_name  # Usar el mismo nombre
                print(f"✗ {dataset_name:50s} → SIN COINCIDENCIA (usando mismo nombre)")
    
    if unmatched:
        print(f"\n⚠ {len(unmatched)} departamentos sin coincidencia:")
        for name in unmatched:
            print(f"  • {name}")
    
    return mapping

def save_mapping(mapping, filename='departamentos_geojson_mapping.json'):
    """Guarda el mapeo en archivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Mapeo guardado en: {filename}")

def save_geojson(geojson_data, filename='colombia.geojson'):
    """Guarda el GeoJSON descargado"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False)
    
    print(f"✓ GeoJSON guardado en: {filename}")

def main():
    print("="*80)
    print("GENERADOR DE MAPEO GEOJSON - DEPARTAMENTOS DE COLOMBIA")
    print("="*80)
    
    # 1. Descargar GeoJSON
    geojson_data = download_geojson()
    
    # 2. Guardar GeoJSON
    save_geojson(geojson_data)
    
    # 3. Extraer nombres de departamentos del GeoJSON
    geojson_names = extract_department_names(geojson_data)
    
    # 4. Nombres del dataset
    dataset_names = list(URBAN_CENTER_COORDS.keys())
    print(f"\n✓ {len(dataset_names)} departamentos en dataset")
    
    # 5. Crear mapeo
    mapping = create_mapping(dataset_names, geojson_names)
    
    # 6. Guardar mapeo
    save_mapping(mapping)
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nArchivos generados:")
    print("  1. colombia.geojson - GeoJSON de Colombia")
    print("  2. departamentos_geojson_mapping.json - Mapeo de nombres")
    print("\nPuedes usar estos archivos en tu aplicación web.")

if __name__ == "__main__":
    main()
