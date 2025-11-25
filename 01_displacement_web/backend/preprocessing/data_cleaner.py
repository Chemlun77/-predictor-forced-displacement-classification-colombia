import pandas as pd
from .category_mappings import (
    ESTADO_DEPTO_MAPPING, ETNIA_MAPPING, CICLO_VITAL_MAPPING, 
    HECHO_MAPPING, VALUES_TO_REMOVE
)

def clean_input_data(data):
    cleaned = data.copy()
    
    if 'ESTADO_DEPTO' in cleaned:
        if cleaned['ESTADO_DEPTO'] in ESTADO_DEPTO_MAPPING:
            cleaned['ESTADO_DEPTO'] = ESTADO_DEPTO_MAPPING[cleaned['ESTADO_DEPTO']]
        if cleaned['ESTADO_DEPTO'] in VALUES_TO_REMOVE['ESTADO_DEPTO']:
            return None
    
    if 'ETNIA' in cleaned:
        if cleaned['ETNIA'] in ETNIA_MAPPING:
            cleaned['ETNIA'] = ETNIA_MAPPING[cleaned['ETNIA']]
    
    if 'CICLO_VITAL' in cleaned:
        if cleaned['CICLO_VITAL'] in CICLO_VITAL_MAPPING:
            cleaned['CICLO_VITAL'] = CICLO_VITAL_MAPPING[cleaned['CICLO_VITAL']]
        if cleaned['CICLO_VITAL'] in VALUES_TO_REMOVE['CICLO_VITAL']:
            return None
    
    if 'SEXO' in cleaned:
        if cleaned['SEXO'] in VALUES_TO_REMOVE['SEXO']:
            return None
    
    if 'DISCAPACIDAD' in cleaned:
        if cleaned['DISCAPACIDAD'] in VALUES_TO_REMOVE['DISCAPACIDAD']:
            return None
    
    if 'HECHO' in cleaned:
        if cleaned['HECHO'] in HECHO_MAPPING:
            cleaned['HECHO'] = HECHO_MAPPING[cleaned['HECHO']]
        if cleaned['HECHO'] in VALUES_TO_REMOVE['HECHO']:
            return None
    
    return cleaned

def clean_api_results(df):
    if df is None or len(df) == 0:
        return df
    
    df = df.copy()
    
    if 'ESTADO_DEPTO' in df.columns:
        df['ESTADO_DEPTO'] = df['ESTADO_DEPTO'].replace(ESTADO_DEPTO_MAPPING)
        df = df[~df['ESTADO_DEPTO'].isin(VALUES_TO_REMOVE['ESTADO_DEPTO'])]
    
    if 'ETNIA' in df.columns:
        df['ETNIA'] = df['ETNIA'].replace(ETNIA_MAPPING)
    
    if 'CICLO_VITAL' in df.columns:
        df['CICLO_VITAL'] = df['CICLO_VITAL'].replace(CICLO_VITAL_MAPPING)
        df = df[~df['CICLO_VITAL'].isin(VALUES_TO_REMOVE['CICLO_VITAL'])]
    
    if 'SEXO' in df.columns:
        df = df[~df['SEXO'].isin(VALUES_TO_REMOVE['SEXO'])]
    
    if 'DISCAPACIDAD' in df.columns:
        df = df[~df['DISCAPACIDAD'].isin(VALUES_TO_REMOVE['DISCAPACIDAD'])]
    
    if 'HECHO' in df.columns:
        df['HECHO'] = df['HECHO'].replace(HECHO_MAPPING)
        df = df[~df['HECHO'].isin(VALUES_TO_REMOVE['HECHO'])]
    
    return df

def get_valid_values():
    return {
        'ESTADO_DEPTO': list(set([v for v in ESTADO_DEPTO_MAPPING.values()] + 
                                 [k for k in ESTADO_DEPTO_MAPPING.keys() if k not in VALUES_TO_REMOVE['ESTADO_DEPTO']])),
        'SEXO': ['Mujer', 'Hombre', 'LGBTI', 'Intersexual'],
        'ETNIA': ['Ninguna', 'Afrocolombiano(a)', 'Indigena', 
                  'Raizal del Archipielago de San Andres y Providencia', 
                  'Gitano(a)', 'Palenquero'],
        'DISCAPACIDAD': ['Ninguna', 'Fisica', 'Psicosocial (Mental)', 'Multiple',
                         'Auditiva', 'Intelectual', 'Visual'],
        'CICLO_VITAL': ['entre 0 y 5', 'entre 6 y 11', 'entre 12 y 17', 
                        'entre 18 y 28', 'entre 29 y 59', 'entre 60 y 110'],
        'VIGENCIA': {'min': 1985, 'max': 2025, 'max_prediction': 2030}
    }
