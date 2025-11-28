"""
Gemini AI Client for Chatbot
Handles communication with Google Gemini API using user-provided API keys
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any

# Training data ranges
TRAINING_RANGES = {
    'VIGENCIA': {'min': 1985, 'max': 2025},
    'EVENTOS': {'min': 0, 'max': 351905}
}

class GeminiClient:
    """Client to interact with Gemini API"""
    
    # List of models to try in order of preference
    MODELS_TO_TRY = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-2.5-pro',
        'models/gemini-flash-latest',
        'models/gemini-pro-latest',
    ]
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini client with user's API key
        
        Args:
            api_key: User's Gemini API key
        """
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model = None
        self.model_name = None
    
    def _get_model(self):
        """Lazy initialization of model - only create when needed"""
        if self.model is not None:
            return self.model
        
        print(f"[Chatbot] Initializing Gemini model...")
        
        for model_name in self.MODELS_TO_TRY:
            try:
                self.model = genai.GenerativeModel(model_name)
                self.model_name = model_name
                print(f"[Chatbot] ✓ Using model: {model_name}")
                return self.model
            except Exception as e:
                print(f"[Chatbot]   Model {model_name} failed: {str(e)[:80]}")
                continue
        
        raise Exception("No Gemini models available with this API key")
    
    def _check_out_of_range(self, user_input: Dict[str, Any]) -> List[str]:
        """Check if VIGENCIA or EVENTOS are outside training ranges"""
        warnings = []
        
        vigencia = user_input.get('VIGENCIA')
        if vigencia:
            vigencia = int(vigencia)
            if vigencia < TRAINING_RANGES['VIGENCIA']['min'] or vigencia > TRAINING_RANGES['VIGENCIA']['max']:
                warnings.append(
                    f"Año: {vigencia} (rango de entrenamiento: {TRAINING_RANGES['VIGENCIA']['min']}-{TRAINING_RANGES['VIGENCIA']['max']})"
                )
        
        eventos = user_input.get('EVENTOS')
        if eventos is not None:
            eventos = int(eventos)
            if eventos < TRAINING_RANGES['EVENTOS']['min'] or eventos > TRAINING_RANGES['EVENTOS']['max']:
                warnings.append(
                    f"Eventos: {eventos:,} (rango de entrenamiento: {TRAINING_RANGES['EVENTOS']['min']}-{TRAINING_RANGES['EVENTOS']['max']:,})"
                )
        
        return warnings
    
    def generate_explanation(
        self,
        user_input: Dict,
        prediction: Dict,
        model_metrics: Dict,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate explanation for the prediction
        
        Args:
            user_input: Input variables used for prediction
            prediction: Model prediction results (includes validation data)
            model_metrics: Metrics of the model used
            conversation_history: Previous messages in conversation
            
        Returns:
            AI-generated explanation
        """
        
        print(f"[Chatbot] Generating explanation...")
        print(f"[Chatbot]   User input: {user_input}")
        print(f"[Chatbot]   Prediction: {prediction}")
        print(f"[Chatbot]   Model: {prediction.get('model', 'Unknown')}")
        
        # Build context prompt
        context = self._build_context(user_input, prediction, model_metrics)
        
        try:
            model = self._get_model()
            
            # Add conversation history if exists
            if conversation_history:
                chat_session = model.start_chat(history=self._format_history(conversation_history))
                response = chat_session.send_message(context)
            else:
                response = model.generate_content(context)
            
            print(f"[Chatbot] ✓ Explanation generated successfully")
            return response.text
            
        except Exception as e:
            print(f"[Chatbot] ✗ Error generating explanation: {e}")
            raise
    
    def chat(self, message: str, context: Dict, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        General chat with context about current prediction
        
        Args:
            message: User's message
            context: Current prediction context
            conversation_history: Previous messages
            
        Returns:
            AI response
        """
        
        print(f"[Chatbot] Processing chat message: {message[:50]}...")
        
        # Build system context
        system_context = self._build_chat_context(context)
        
        # Combine system context with user message
        full_prompt = f"""{system_context}

User question: {message}

Please provide a clear, concise answer based on the prediction context above. Use specific numbers and data when relevant."""
        
        try:
            model = self._get_model()
            
            if conversation_history:
                chat_session = model.start_chat(history=self._format_history(conversation_history))
                response = chat_session.send_message(full_prompt)
            else:
                response = model.generate_content(full_prompt)
            
            print(f"[Chatbot] ✓ Chat response generated")
            return response.text
            
        except Exception as e:
            print(f"[Chatbot] ✗ Error in chat: {e}")
            raise
    
    def _build_context(self, user_input: Dict, prediction: Dict, model_metrics: Dict) -> str:
        """Build structured context for initial explanation"""
        
        # Extract prediction details
        model_name = prediction.get('model', 'Unknown')
        predicted_class = prediction.get('prediction', 'Unknown')
        predicted_label = prediction.get('label', 'Unknown')
        
        # Check for out-of-range values
        range_warnings = self._check_out_of_range(user_input)
        
        # Get geographic values
        km_norte_sur = user_input.get('km_norte_sur', 'N/A')
        km_este_oeste = user_input.get('km_este_oeste', 'N/A')
        distancia_total = user_input.get('distancia_total', 'N/A')
        
        # Build base context
        context = f"""Eres un analista experto en patrones de desplazamiento forzado en el conflicto armado colombiano.
Tienes acceso a un modelo de machine learning entrenado con más de 7 millones de registros del Registro Único de Víctimas (RUV).

NOTA METODOLÓGICA:

El modelo fue entrenado con datos del RUV procesados con las siguientes transformaciones:

1. Variable objetivo: Clasificación binaria (Desplazamiento Forzado vs Otros Hechos Victimizantes)

2. Variables eliminadas por redundancia o falta de variabilidad:
   - Metadatos temporales: FECHA_CORTE, NOM_RPT
   - Identificadores redundantes: COD_PAIS, PAIS, COD_ESTADO_DEPTO, PARAM_HECHO
   - Variables correlacionadas: PER_OCU y PER_DECLA (correlación >0.9 con EVENTOS)

3. Categorías agrupadas y corregidas:
   - Etnias: Unificación de categorías de acreditación
   - Departamentos: Corrección de errores tipográficos y caracteres mal codificados
   - Hechos victimizantes: Corrección de acentos y caracteres especiales

4. Registros excluidos para mejorar calidad:
   - Valores indeterminados: Sexo "No Informa", Departamento "SIN DEFINIR", 
     Ciclo Vital "ND", Discapacidad "Por Establecer", Hecho "Sin informacion"

5. Correcciones de rangos etarios:
   - "entre 29 y 60" → "entre 29 y 59"
   - "entre 61 y 100" → "entre 60 y 110"

6. Variables geográficas agregadas:
   Las variables geográficas capturan patrones espaciales del conflicto armado colombiano.
   Se calculan usando las coordenadas de las capitales departamentales respecto a Bogotá D.C.:
   
   - Distancia Norte-Sur: Mide la separación geodésica entre cada capital departamental y Bogotá 
     en el eje norte-sur. Valores negativos indican ubicaciones al sur de Bogotá.
   
   - Distancia Este-Oeste: Mide la separación geodésica entre cada capital departamental y Bogotá 
     en el eje este-oeste. Valores negativos indican ubicaciones al oeste de Bogotá.
   
   - Distancia Total: Captura la distancia geodésica total desde Bogotá, usada como indicador de 
     "distancia al Estado" y alcance institucional.
   
   Estas variables ayudan al modelo a identificar patrones relacionados con presencia estatal, 
   corredores de movilidad estratégica y exposición a economías ilícitas y están agregadas por 
   defecto al seleccionar un departamento lo que da contexto del espacio geográfico y ayuda al 
   modelo a mejorar las predicciones al tener información relevante de todo el mapa de Colombia.

PREDICCIÓN ACTUAL:

Variables de entrada:
- Departamento: {user_input.get('ESTADO_DEPTO', 'N/A')}
- Género: {user_input.get('SEXO', 'N/A')}
- Etnia: {user_input.get('ETNIA', 'N/A')}
- Discapacidad: {user_input.get('DISCAPACIDAD', 'N/A')}
- Rango de edad: {user_input.get('CICLO_VITAL', 'N/A')}
- Año: {user_input.get('VIGENCIA', 'N/A')}
- Eventos previos: {user_input.get('EVENTOS', 'N/A')}

Variables geográficas (desde Bogotá D.C.):
- Distancia Norte-Sur: {km_norte_sur} km
- Distancia Este-Oeste: {km_este_oeste} km
- Distancia Total: {distancia_total} km

RESULTADO DEL MODELO:
- Modelo: {model_name}
- Predicción: {predicted_label} (Clase {predicted_class})

RENDIMIENTO DEL MODELO:
- Accuracy: {model_metrics.get('accuracy', 0)*100:.2f}%
- Precision: {model_metrics.get('precision', 0)*100:.2f}%
- Recall: {model_metrics.get('recall', 0)*100:.2f}%
- F1-Score: {model_metrics.get('f1_score', 0)*100:.2f}%
- ROC-AUC: {model_metrics.get('roc_auc', 0)*100:.2f}%
"""
        
        # Add out-of-range warning if applicable
        if range_warnings:
            context += f"""
ADVERTENCIA - VALORES FUERA DE RANGO DE ENTRENAMIENTO:
Los siguientes valores están fuera del rango histórico del dataset:
"""
            for warning in range_warnings:
                context += f"  - {warning}\n"
            context += """
Esto puede afectar la confiabilidad de la predicción ya que el modelo no fue entrenado con datos en estos rangos.
"""
        
        # Add validation information if present
        match_type = prediction.get('match_type')
        
        if match_type == 'exact_match':
            real_label = prediction.get('real_label', 'Unknown')
            is_correct = prediction.get('is_correct', False)
            matches_data = prediction.get('matches_data', [])
            
            context += f"""
VALIDACIÓN CON DATOS OFICIALES DEL RUV:
Se encontró coincidencia exacta en el dataset.
"""
            if matches_data and len(matches_data) > 0:
                real_record = matches_data[0]
                context += f"""
Registro real del RUV con estas características:
- Departamento: {real_record.get('estado_depto', real_record.get('ESTADO_DEPTO', 'N/A'))}
- Género: {real_record.get('sexo', real_record.get('SEXO', 'N/A'))}
- Etnia: {real_record.get('etnia', real_record.get('ETNIA', 'N/A'))}
- Discapacidad: {real_record.get('discapacidad', real_record.get('DISCAPACIDAD', 'N/A'))}
- Rango de edad: {real_record.get('ciclo_vital', real_record.get('CICLO_VITAL', 'N/A'))}
- Año: {real_record.get('vigencia', real_record.get('VIGENCIA', 'N/A'))}
- Eventos: {real_record.get('eventos', real_record.get('EVENTOS', 'N/A'))}
- Hecho real: {real_record.get('hecho', real_record.get('HECHO', 'N/A'))}

"""
            context += f"Clasificación real en el RUV: {real_label}\n"
            if is_correct:
                context += "→ La predicción del modelo COINCIDE con los datos reales\n"
            else:
                context += "→ La predicción del modelo NO COINCIDE con los datos reales\n"
        
        elif match_type == 'ambiguous':
            displacement_count = prediction.get('displacement_count', 0)
            other_count = prediction.get('other_count', 0)
            total = displacement_count + other_count
            matches_data = prediction.get('matches_data', [])
            
            context += f"""
VALIDACIÓN CON DATOS OFICIALES DEL RUV:
Se detectó ambigüedad ({total} coincidencias encontradas):
- Desplazamiento Forzado: {displacement_count} casos
- Otros Hechos Victimizantes: {other_count} casos

Razón de la ambigüedad: El dataset carece de suficiente granularidad (ej: datos a nivel municipal
o fechas exactas) para distinguir entre estos casos. Esto refleja limitaciones de los datos 
agregados a nivel departamental.
"""
            
            # Show sample records if available
            if matches_data and len(matches_data) > 0:
                context += "\nEjemplos de registros reales encontrados:\n"
                for i, record in enumerate(matches_data[:3], 1):  # Show first 3
                    hecho = record.get('hecho', record.get('HECHO', 'N/A'))
                    context += f"{i}. Hecho: {hecho}\n"
        
        elif match_type == 'no_match':
            context += """
VALIDACIÓN CON DATOS OFICIALES DEL RUV:
No se encontró coincidencia exacta en el dataset.
Esta combinación de variables no aparece en los registros históricos del RUV, por lo que la 
predicción no puede validarse con datos reales.
"""
        
        # Add map context
        context += """

MAPA INTERACTIVO:
La aplicación incluye un mapa interactivo de Colombia que muestra el departamento seleccionado 
resaltado. Este mapa permite visualizar la ubicación geográfica del departamento en el contexto 
nacional, lo cual es relevante para entender los patrones espaciales del conflicto.
"""
        
        # Task instructions
        context += """
INSTRUCCIONES:
Proporciona una explicación clara y concisa en español. IMPORTANTE: NO uses markdown, asteriscos ni 
símbolos para formato. Usa SOLO texto plano.

Incluye:

1. INTERPRETACIÓN: Explica qué significa el resultado de forma clara y directa

2. FACTORES CLAVE: Menciona las variables más relevantes que influyeron en la predicción
   (incluye las variables geográficas cuando sean significativas)

3. VALIDACIÓN: Explica qué muestran los datos reales del RUV:
   - Si hay coincidencia exacta: describe el registro real encontrado
   - Si hay ambigüedad: explica la distribución de casos y la razón
   - Si no hay coincidencia: menciona esta limitación

4. CONTEXTO: Si hay advertencias sobre valores fuera de rango, explica las implicaciones

Usa un tono profesional pero accesible. Sé preciso con los números. Mantén la explicación 
CONCISA (máximo 400 palabras). NO menciones niveles de confianza. Responde en español.
NO uses formato markdown (nada de asteriscos, guiones, ni símbolos especiales).
"""
        
        return context
    
    def _build_chat_context(self, context: Dict) -> str:
        """Build context for general chat"""
        
        user_input = context.get('userInput', {})
        prediction = context.get('prediction', {})
        model_metrics = context.get('modelMetrics', {})
        
        model_name = prediction.get('model', 'Unknown')
        predicted_class = prediction.get('prediction', 'Unknown')
        predicted_label = prediction.get('label', 'Unknown')
        
        chat_context = f"""Eres un asistente de IA que ayuda a los usuarios a entender predicciones de un modelo
de clasificación de desplazamiento forzado entrenado con el Registro Único de Víctimas (RUV) de Colombia.

CONTEXTO DE LA PREDICCIÓN ACTUAL:

Entrada:
- Departamento: {user_input.get('ESTADO_DEPTO')}
- Género: {user_input.get('SEXO')}
- Etnia: {user_input.get('ETNIA')}
- Edad: {user_input.get('CICLO_VITAL')}
- Año: {user_input.get('VIGENCIA')}
- Eventos: {user_input.get('EVENTOS')}

Variables Geográficas:
- Norte-Sur: {user_input.get('km_norte_sur', 'N/A')} km desde Bogotá
- Este-Oeste: {user_input.get('km_este_oeste', 'N/A')} km desde Bogotá
- Distancia Total: {user_input.get('distancia_total', 'N/A')} km desde Bogotá

Predicción: {predicted_label} (Clase {predicted_class})
Modelo: {model_name} (Accuracy: {model_metrics.get('accuracy', 0)*100:.1f}%, ROC-AUC: {model_metrics.get('roc_auc', 0)*100:.1f}%)

Responde preguntas basándote en este contexto de predicción. Sé conciso, preciso y útil. Responde en español."""

        return chat_context
    
    def _format_history(self, history: List[Dict]) -> List[Dict]:
        """Format conversation history for Gemini API"""
        
        formatted = []
        for msg in history:
            role = msg.get("role", "user")
            # Gemini API uses "model" instead of "assistant"
            if role == "assistant":
                role = "model"
            
            formatted.append({
                "role": role,
                "parts": [msg.get("content", "")]
            })
        
        return formatted


def test_gemini_connection(api_key: str) -> Dict:
    """
    Test if API key is valid by trying to configure and list models
    
    Args:
        api_key: Gemini API key to test
        
    Returns:
        Dict with 'valid' (bool) and 'message' (str)
    """
    
    try:
        print(f"[Chatbot] Testing API key...")
        genai.configure(api_key=api_key)
        
        # Simple test - try to list models (lightweight operation)
        models = list(genai.list_models())
        
        if len(models) > 0:
            print(f"[Chatbot] ✓ API key valid - {len(models)} models available")
            return {
                "valid": True,
                "message": f"API key is valid ({len(models)} models available)"
            }
        else:
            print(f"[Chatbot] ✗ API key valid but no models found")
            return {
                "valid": False,
                "message": "API key is valid but no models are available"
            }
    
    except Exception as e:
        print(f"[Chatbot] ✗ API key test failed: {e}")
        return {
            "valid": False,
            "message": f"Invalid API key: {str(e)}"
        }