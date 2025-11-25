# Predictor de Clasificación de Desplazamiento Forzado - Conflicto Armado en Colombia

Aplicación web para predecir y clasificar eventos de desplazamiento forzado en Colombia usando modelos de machine learning entrenados con datos del Registro Único de Víctimas (RUV).

## Estructura del Proyecto
```
project_00_RUV_displacement/
├── 00_predictive_displacement_model/    # Notebooks y scripts de entrenamiento
└── 01_displacement_web/                 # Aplicación web
    ├── backend/                         # API Flask
    ├── frontend/                        # Interfaz React
    └── db/                              # Modelos entrenados (descargar aparte)
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Descargar modelos entrenados

**Los modelos NO están en el repositorio por su tamaño. Descárgalos desde Google Drive:**

- **Modelos clásicos (3.9 GB):** [Descargar aquí](https://drive.google.com/file/d/10HN9Wv-u6i2FT6Kb5QrOgDib_9XKvs1L/view?usp=sharing)
- **Redes neuronales (13 MB):** [Descargar aquí](https://drive.google.com/file/d/1-Q2-kcODg225sMGdWnTOJ3Y_5fWYgMDI/view?usp=sharing)

**Extraer en la ubicación correcta:**
```bash
cd 01_displacement_web/db

# Extraer modelos clásicos
tar -xzf modelos_clasicos.tar.gz

# Extraer redes neuronales
tar -xzf modelos_redes_neuronales.tar.gz
```

**Estructura final esperada:**
```
01_displacement_web/db/
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

### 3. Instalar dependencias del backend
```bash
cd 01_displacement_web/backend

# Crear ambiente conda
conda create -n displacement python=3.10 -y
conda activate displacement

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Instalar dependencias del frontend
```bash
cd ../frontend
npm install
```

## Ejecución

### Terminal 1 - Backend:
```bash
cd 01_displacement_web/backend
conda activate displacement
python app.py
```

Backend corriendo en: http://127.0.0.1:5000

### Terminal 2 - Frontend:
```bash
cd 01_displacement_web/frontend
npm start
```

Aplicación disponible en: http://localhost:3000

## Tecnologías

**Backend:**
- Python 3.10
- Flask 3.0
- TensorFlow 2.20
- Scikit-learn 1.7.2
- XGBoost 2.1.0
- Pandas 2.2+
- Sodapy (API Socrata)

**Frontend:**
- React 18
- Leaflet (mapas)
- Axios

## Modelos

- **Logistic Regression**
- **Random Forest**
- **XGBoost**
- **ResNet Style (Red Neuronal)**
- **Deep - Wide & Deep (Red Neuronal)**

## Datos

Fuente: [Registro Único de Víctimas - datos.gov.co](https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Registro-nico-de-V-ctimas-RUV-a-nivel-nacional-/dyjp-uwwh)

## Autor

Fabian Luna - Universidad Nacional de Colombia

## Licencia

Este proyecto es de código abierto para fines educativos y de investigación.
