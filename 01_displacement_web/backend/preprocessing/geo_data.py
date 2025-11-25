from geopy.distance import geodesic

DEPT_CAPITALS = {
    'Amazonas': 'Leticia', 'Antioquia': 'Medellín', 'Arauca': 'Arauca',
    'Atlantico': 'Barranquilla', 'Bolivar': 'Cartagena', 'Boyaca': 'Tunja',
    'Caldas': 'Manizales', 'Caqueta': 'Florencia', 'Casanare': 'Yopal',
    'Cauca': 'Popayán', 'Cesar': 'Valledupar', 'Choco': 'Quibdó',
    'Cordoba': 'Montería', 'Cundinamarca': 'Bogotá', 'Guainia': 'Inírida',
    'Guaviare': 'San José del Guaviare', 'Huila': 'Neiva', 'La Guajira': 'Riohacha',
    'Magdalena': 'Santa Marta', 'Meta': 'Villavicencio', 'Nariño': 'Pasto',
    'Norte De Santander': 'Cúcuta', 'Putumayo': 'Mocoa', 'Quindio': 'Armenia',
    'Risaralda': 'Pereira', 'Archipielago de San Andrés, Providencia y Santa Catalina': 'San Andrés',
    'Santander': 'Bucaramanga', 'Sucre': 'Sincelejo', 'Tolima': 'Ibagué',
    'Valle del Cauca': 'Cali', 'Vaupes': 'Mitú', 'Vichada': 'Puerto Carreño',
    'Bogota, D.C.': 'Bogotá'
}

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

BOGOTA_COORDS = (4.5981, -74.0758)

def calculate_distances(dept_name):
    coords = URBAN_CENTER_COORDS.get(dept_name)
    
    if not coords:
        return {
            'km_norte_sur': 0,
            'km_este_oeste': 0,
            'distancia_total': 0
        }
    
    lat, lon = coords
    
    km_norte_sur = geodesic(BOGOTA_COORDS, (lat, BOGOTA_COORDS[1])).km
    if lat < BOGOTA_COORDS[0]:
        km_norte_sur = -km_norte_sur
    
    km_este_oeste = geodesic(BOGOTA_COORDS, (BOGOTA_COORDS[0], lon)).km
    if lon < BOGOTA_COORDS[1]:
        km_este_oeste = -km_este_oeste
    
    distancia_total = geodesic(BOGOTA_COORDS, coords).km
    
    return {
        'km_norte_sur': round(km_norte_sur, 2),
        'km_este_oeste': round(km_este_oeste, 2),
        'distancia_total': round(distancia_total, 2)
    }

def get_department_info(dept_name):
    coords = URBAN_CENTER_COORDS.get(dept_name)
    if not coords:
        return None
    
    lat, lon = coords
    distances = calculate_distances(dept_name)
    
    return {
        'department': dept_name,
        'capital': DEPT_CAPITALS.get(dept_name, ''),
        'lat': lat,
        'lon': lon,
        **distances
    }
