# Predictor de Desplazamiento Forzado - Conflicto Armado Colombia

Aplicación web para predecir desplazamiento forzado en Colombia usando modelos de machine learning.

## Estructura del Proyecto

```
proyecto/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── preprocessing/
│   │   ├── category_mappings.py
│   │   ├── data_cleaner.py
│   │   └── geo_data.py
│   ├── api/
│   │   └── socrata_client.py
│   └── prediction/
│       └── predictor.py
│
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.js
│       ├── components/
│       │   ├── ControlPanel.jsx/css
│       │   ├── MapView.jsx/css
│       │   ├── ModelSelector.jsx/css
│       │   ├── VariableInputs.jsx/css
│       │   └── PredictionResult.jsx/css
│       ├── services/
│       │   └── apiService.js
│       └── utils/
│           └── constants.js
│
└── db/
    ├── 02a_classical_models/saved_models/
    │   ├── Logistic_Regression_best_model.pkl
    │   ├── Random_Forest_best_model.pkl
    │   ├── XGBoost_best_model.pkl
    │   ├── categorical_encoders.pkl
    │   └── numeric_scalers.pkl
    └── 02b_neural_networks/saved_models/
        ├── ResNet_Style_best_model.keras
        ├── Deep_best_model.keras
        ├── categorical_encoders.pkl
        ├── embedding_info.pkl
        └── numeric_scalers.pkl
```

## Requisitos Previos

- Python 3.9+
- Node.js 18+
- Modelos entrenados en la carpeta `db/` (según estructura arriba)

## Instalación

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Ejecución Local

### 1. Iniciar Backend

```bash
cd backend
python app.py
```

El backend estará disponible en `http://localhost:5000`

### 2. Iniciar Frontend

```bash
cd frontend
npm start
```

El frontend estará disponible en `http://localhost:3000`

## Uso

1. Selecciona un modelo de machine learning
2. Completa las variables predictoras:
   - Variables categóricas (departamento, sexo, etnia, etc.)
   - Variables numéricas (año, eventos)
   - Variables geográficas (se auto-llenan al seleccionar departamento)
3. Presiona "Predecir"
4. El resultado mostrará:
   - Predicción del modelo
   - Validación con datos reales (si existe coincidencia)
   - Visualización en el mapa de Colombia

## Características

- 5 modelos de ML (3 clásicos + 2 redes neuronales)
- Validación contra API de datos abiertos de Colombia
- Mapa interactivo con Leaflet
- Cálculo automático de distancias geográficas
- Manejo de ambigüedad en datos

## Deployment a Dominio

### Opción 1: Heroku (Backend + Frontend)

1. Crear archivo `Procfile` en raíz:
```
web: cd backend && gunicorn app:app
```

2. Instalar gunicorn:
```bash
pip install gunicorn
pip freeze > backend/requirements.txt
```

3. Deploy:
```bash
heroku create nombre-app
git push heroku main
```

### Opción 2: Vercel (Frontend) + Render (Backend)

**Backend en Render:**
1. Conectar repositorio
2. Build command: `pip install -r requirements.txt`
3. Start command: `python app.py`

**Frontend en Vercel:**
1. Conectar repositorio
2. Root directory: `frontend`
3. Build command: `npm run build`
4. Actualizar `API_BASE_URL` en `constants.js` con URL del backend

### Opción 3: VPS (DigitalOcean, AWS EC2)

```bash
# Backend
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend (build)
cd frontend
npm run build
# Servir con nginx
```

## Notas Importantes

- Los modelos deben estar en la carpeta `db/` según estructura indicada
- La API de Socrata puede tener límites de rate (1000 registros por query)
- Para producción, configurar variables de entorno para API keys
- Activar CORS en backend para dominio específico

## Autores

Fabian - Universidad Nacional de Colombia
