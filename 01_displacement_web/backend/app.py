from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocessing.data_cleaner import clean_input_data, clean_api_results, get_valid_values
from preprocessing.geo_data import get_department_info, URBAN_CENTER_COORDS, DEPT_CAPITALS
from api.socrata_client import SocrataClient
from prediction.predictor import ModelPredictor

app = Flask(__name__)
CORS(app)

predictor = ModelPredictor()
socrata_client = SocrataClient()

@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({
        'models': [
            {'name': 'Logistic_Regression', 'display': 'Logistic Regression'},
            {'name': 'Random_Forest', 'display': 'Random Forest'},
            {'name': 'XGBoost', 'display': 'XGBoost'},
            {'name': 'ResNet_Style', 'display': 'ResNet Style'},
            {'name': 'Deep', 'display': 'Deep (Wide & Deep)'}
        ]
    })

@app.route('/api/variables', methods=['GET'])
def get_variables():
    valid_values = get_valid_values()
    
    return jsonify({
        'categorical': {
            'ESTADO_DEPTO': sorted(list(URBAN_CENTER_COORDS.keys())),
            'SEXO': valid_values['SEXO'],
            'ETNIA': valid_values['ETNIA'],
            'DISCAPACIDAD': valid_values['DISCAPACIDAD'],
            'CICLO_VITAL': valid_values['CICLO_VITAL']
        },
        'numeric': {
            'VIGENCIA': valid_values['VIGENCIA'],
            'EVENTOS': {'min': 1, 'max': 10000}
        }
    })

@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = []
    for dept_name in URBAN_CENTER_COORDS.keys():
        info = get_department_info(dept_name)
        if info:
            departments.append(info)
    
    return jsonify({'departments': departments})

@app.route('/api/department_geo/<dept_name>', methods=['GET'])
def get_department_geometry(dept_name):
    info = get_department_info(dept_name)
    
    if not info:
        return jsonify({'error': 'Department not found'}), 404
    
    return jsonify(info)

@app.route('/api/validate_year', methods=['POST'])
def validate_year():
    data = request.json
    year = data.get('year')
    
    if not year:
        return jsonify({'valid': False, 'warning': 'Year is required'}), 400
    
    year = int(year)
    MIN_YEAR = 1985
    MAX_YEAR = 2025
    MAX_PREDICTION = 2030
    
    if year < MIN_YEAR or year > MAX_PREDICTION:
        return jsonify({
            'valid': False,
            'warning': f'Año debe estar entre {MIN_YEAR} y {MAX_PREDICTION}'
        })
    elif year > MAX_YEAR:
        return jsonify({
            'valid': True,
            'warning': f'⚠ Predicción para año futuro ({year})'
        })
    else:
        return jsonify({'valid': True, 'warning': None})

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    
    model_name = data.get('model')
    input_data = {
        'ESTADO_DEPTO': data.get('ESTADO_DEPTO'),
        'SEXO': data.get('SEXO'),
        'ETNIA': data.get('ETNIA'),
        'DISCAPACIDAD': data.get('DISCAPACIDAD'),
        'CICLO_VITAL': data.get('CICLO_VITAL'),
        'VIGENCIA': int(data.get('VIGENCIA')),
        'EVENTOS': int(data.get('EVENTOS')),
        'km_norte_sur': float(data.get('km_norte_sur')),
        'km_este_oeste': float(data.get('km_este_oeste')),
        'distancia_total': float(data.get('distancia_total'))
    }
    
    cleaned_input = clean_input_data(input_data)
    if cleaned_input is None:
        return jsonify({'error': 'Invalid input data'}), 400
    
    try:
        prediction_result = predictor.predict(model_name, cleaned_input)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    filters = {
        'ESTADO_DEPTO': input_data['ESTADO_DEPTO'],
        'SEXO': input_data['SEXO'],
        'ETNIA': input_data['ETNIA'],
        'DISCAPACIDAD': input_data['DISCAPACIDAD'],
        'CICLO_VITAL': input_data['CICLO_VITAL'],
        'VIGENCIA': input_data['VIGENCIA'],
        'EVENTOS': input_data['EVENTOS']
    }
    
    try:
        matches_df = socrata_client.query_exact_match(filters)
        matches_df = clean_api_results(matches_df)
    except Exception as e:
        print(f"Error querying API: {e}")
        matches_df = None
    
    validation_result = analyze_matches(matches_df, prediction_result)
    
    return jsonify({
        **prediction_result,
        **validation_result
    })

def analyze_matches(matches_df, prediction_result):
    if matches_df is None or len(matches_df) == 0:
        return {
            'match_type': 'no_match',
            'message': '⚠ No hay coincidencia exacta en el dataset',
            'submessage': 'Se realizará la predicción sin validación'
        }
    
    displacement_count = 0
    other_count = 0
    
    # Debug: imprimir primeras filas
    print("\n=== PRIMERAS 3 FILAS DE RESULTADOS ===")
    for idx, row in matches_df.head(3).iterrows():
        print(f"Row {idx}:")
        print(f"  Columnas disponibles: {list(row.keys())}")
        if 'hecho' in row:
            print(f"  hecho: {row['hecho']}")
        if 'HECHO' in row:
            print(f"  HECHO: {row['HECHO']}")
        print()
    print("=" * 50)
    
    for _, row in matches_df.iterrows():
        # Intentar ambos nombres de columna
        hecho = str(row.get('hecho', row.get('HECHO', ''))).lower()
        
        if 'desplazamiento forzado' in hecho:
            displacement_count += 1
        else:
            other_count += 1
    
    total_matches = len(matches_df)
    
    if total_matches == 1:
        real_value = 1 if displacement_count > 0 else 0
        predicted_value = prediction_result['prediction']
        is_correct = (real_value == predicted_value)
        
        real_label = 'Desplazamiento Forzado' if real_value == 1 else 'Otro Hecho Victimizante'
        
        return {
            'match_type': 'exact_match',
            'message': '✓ Coincidencia encontrada en el dataset',
            'real_value': real_value,
            'real_label': real_label,
            'is_correct': is_correct
        }
    else:
        return {
            'match_type': 'ambiguous',
            'message': f'⚠ Ambigüedad detectada ({total_matches} coincidencias)',
            'displacement_count': displacement_count,
            'other_count': other_count,
            'submessage': 'Se requiere mayor granularidad en los datos (ej: información a nivel municipal)'
        }

@app.route('/api/random', methods=['GET'])
def get_random_values():
    import random
    
    valid_values = get_valid_values()
    departments = list(URBAN_CENTER_COORDS.keys())
    dept = random.choice(departments)
    geo_info = get_department_info(dept)
    
    return jsonify({
        'ESTADO_DEPTO': dept,
        'SEXO': random.choice(valid_values['SEXO']),
        'ETNIA': random.choice(valid_values['ETNIA']),
        'DISCAPACIDAD': random.choice(valid_values['DISCAPACIDAD']),
        'CICLO_VITAL': random.choice(valid_values['CICLO_VITAL']),
        'VIGENCIA': random.randint(1985, 2025),
        'EVENTOS': random.randint(1, 1000),
        'km_norte_sur': geo_info['km_norte_sur'],
        'km_este_oeste': geo_info['km_este_oeste'],
        'distancia_total': geo_info['distancia_total']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
