from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocessing.data_cleaner import clean_input_data, clean_api_results, get_valid_values
from preprocessing.geo_data import get_department_info, URBAN_CENTER_COORDS, DEPT_CAPITALS
from api.socrata_client import SocrataClient
from prediction.predictor import ModelPredictor
from chatbot.gemini_client import GeminiClient, test_gemini_connection

app = Flask(__name__)
CORS(app)

predictor = ModelPredictor()
socrata_client = SocrataClient()

# =============================================================================
# MODEL METRICS - For chatbot context
# =============================================================================
MODEL_METRICS = {
    'Logistic_Regression': {
        'accuracy': 0.7416,
        'precision': 0.6305,
        'recall': 0.7471,
        'f1_score': 0.6839,
        'roc_auc': 0.8185
    },
    'Random_Forest': {
        'accuracy': 0.9188,
        'precision': 0.8712,
        'recall': 0.9187,
        'f1_score': 0.8943,
        'roc_auc': 0.9822
    },
    'XGBoost': {
        'accuracy': 0.8629,
        'precision': 0.7818,
        'recall': 0.8788,
        'f1_score': 0.8274,
        'roc_auc': 0.9510
    },
    'ResNet_Style': {
        'accuracy': 0.8673,
        'precision': 0.9822,
        'recall': 0.6572,
        'f1_score': 0.7875,
        'roc_auc': 0.9622
    },
    'Deep': {
        'accuracy': 0.8261,
        'precision': 0.9716,
        'recall': 0.5512,
        'f1_score': 0.7034,
        'roc_auc': 0.9438
    }
}

# =============================================================================
# EXISTING ENDPOINTS
# =============================================================================

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
    
    # Check if Random Forest is requested (may not be available in deployment)
    if model_name == 'Random_Forest':
        try:
            # Try to load Random Forest - will fail if model file doesn't exist
            test_predict = predictor.predict(model_name, None, check_only=True)
        except:
            return jsonify({
                'error': 'El modelo Random Forest no está disponible en este deployment.',
                'message': 'El modelo Random Forest (3,9 GB) se excluye del deployment debido a las limitaciones de memoria del nivel gratuito. Utilice uno de los otros modelos disponibles: regresión logística, XGBoost, ResNet-Style o Deep.',
                'available_models': ['Logistic_Regression', 'XGBoost', 'ResNet_Style', 'Deep']
            }), 503
    
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
    except FileNotFoundError as e:
        # Handle case where model file is missing (Random Forest in deployment)
        if 'Random_Forest' in str(e):
            return jsonify({
                'error': 'El modelo Random Forest no está disponible.',
                'message': 'El modelo Random Forest (3,9 GB) se excluye del deployment debido a limitaciones de memoria. Utilice Logistic Regression, XGBoost, ResNet-Style o Deep.',
                'available_models': ['Logistic_Regression', 'XGBoost', 'ResNet_Style', 'Deep']
            }), 503
        return jsonify({'error': f'Model error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Add label
    label = 'Desplazamiento Forzado' if prediction_result['prediction'] == 1 else 'Otro Hecho Victimizante'
    prediction_result['label'] = label
    
    # Add confidence (same as probability)
    prediction_result['confidence'] = prediction_result['probability']
    
    # Add model name for chatbot
    prediction_result['model'] = model_name
    
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
    
    # Add matches data for chatbot
    if matches_df is not None and len(matches_df) > 0:
        validation_result['matches_data'] = matches_df.to_dict('records')
    
    return jsonify({
        **prediction_result,
        **validation_result,
        'userInput': input_data  # Add for chatbot
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

# =============================================================================
# CHATBOT ENDPOINTS
# =============================================================================

@app.route('/api/chat/test-key', methods=['POST'])
def test_api_key():
    """Test if Gemini API key is valid"""
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required'
            }), 400
        
        # Test the key
        result = test_gemini_connection(api_key)
        
        return jsonify({
            'success': result['valid'],
            'message': result['message']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat/explain', methods=['POST'])
def explain_prediction():
    """Generate AI explanation for a prediction"""
    try:
        data = request.json
        print(f"\n{'='*60}")
        print(f"[EXPLAIN ENDPOINT] Request received")
        print(f"{'='*60}")
        
        api_key = data.get('api_key')
        user_input = data.get('user_input')
        prediction = data.get('prediction')
        model_name = data.get('model_name')
        
        print(f"[EXPLAIN] Has API key: {bool(api_key)}")
        print(f"[EXPLAIN] User input: {user_input}")
        print(f"[EXPLAIN] Prediction: {prediction}")
        print(f"[EXPLAIN] Model name: {model_name}")
        
        if not api_key:
            print(f"[EXPLAIN] ✗ No API key provided")
            return jsonify({
                'success': False,
                'error': 'API key is required'
            }), 400
        
        if not user_input or not prediction or not model_name:
            print(f"[EXPLAIN] ✗ Missing required data")
            print(f"  - user_input: {bool(user_input)}")
            print(f"  - prediction: {bool(prediction)}")
            print(f"  - model_name: {bool(model_name)}")
            return jsonify({
                'success': False,
                'error': 'Missing required data'
            }), 400
        
        # Get model metrics
        model_metrics = MODEL_METRICS.get(model_name, {})
        print(f"[EXPLAIN] Model metrics loaded: {bool(model_metrics)}")
        
        # Initialize Gemini client
        print(f"[EXPLAIN] Initializing Gemini client...")
        client = GeminiClient(api_key)
        
        # Generate explanation
        print(f"[EXPLAIN] Calling generate_explanation...")
        explanation = client.generate_explanation(
            user_input=user_input,
            prediction=prediction,
            model_metrics=model_metrics
        )
        
        print(f"[EXPLAIN] ✓ Success! Explanation length: {len(explanation)} chars")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'explanation': explanation
        })
    
    except Exception as e:
        print(f"[EXPLAIN] ✗ Error: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[EXPLAIN] Traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """Handle chat messages with context"""
    try:
        data = request.json
        api_key = data.get('api_key')
        message = data.get('message')
        context = data.get('context')
        conversation_history = data.get('conversation_history', [])
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required'
            }), 400
        
        if not message or not context:
            return jsonify({
                'success': False,
                'error': 'Message and context are required'
            }), 400
        
        # Initialize Gemini client
        client = GeminiClient(api_key)
        
        # Generate response
        response_text = client.chat(
            message=message,
            context=context,
            conversation_history=conversation_history
        )
        
        return jsonify({
            'success': True,
            'response': response_text
        })
    
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# RUN APP
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)