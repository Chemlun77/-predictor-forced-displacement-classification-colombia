# Forced Displacement Classification Predictor - Armed Conflict in Colombia

Web application to predict and classify forced displacement events in Colombia using machine learning models trained with data from the Unique Registry of Victims (RUV).

## Project Structure
```
project_00_RUV_displacement/
├── 00_predictive_displacement_model/    # Training notebooks and scripts
└── 01_displacement_web/                 # Web application
    ├── backend/                         # Flask API
    ├── frontend/                        # React interface
    └── db/                              # Trained models (download separately)
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Chemlun77/-predictor-forced-displacement-classification-colombia.git
cd -predictor-forced-displacement-classification-colombia
```

### 2. Download trained models

**Models are NOT included in the repository due to their size. Download them from Google Drive:**

- **Classical models (3.9 GB):** [Download here](https://drive.google.com/file/d/10HN9Wv-u6i2FT6Kb5QrOgDib_9XKvs1L/view?usp=sharing)
- **Neural networks (13 MB):** [Download here](https://drive.google.com/file/d/1-Q2-kcODg225sMGdWnTOJ3Y_5fWYgMDI/view?usp=sharing)

**Extract to the correct location:**
```bash
cd 01_displacement_web/db

# Extract classical models
tar -xzf modelos_clasicos.tar.gz

# Extract neural networks
tar -xzf modelos_redes_neuronales.tar.gz
```

**Expected final structure:**
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

### 3. Install backend dependencies
```bash
cd 01_displacement_web/backend

# Create conda environment
conda create -n displacement python=3.10 -y
conda activate displacement

# Install dependencies
pip install -r requirements.txt
```

### 4. Install frontend dependencies
```bash
cd ../frontend
npm install
```

## Running the Application

### Terminal 1 - Backend:
```bash
cd 01_displacement_web/backend
conda activate displacement
python app.py
```

Backend running at: http://127.0.0.1:5000

### Terminal 2 - Frontend:
```bash
cd 01_displacement_web/frontend
npm start
```

Application available at: http://localhost:3000

## Technologies

**Backend:**
- Python 3.10
- Flask 3.0
- TensorFlow 2.20
- Scikit-learn 1.7.2
- XGBoost 2.1.0
- Pandas 2.2+
- Sodapy (Socrata API)

**Frontend:**
- React 18
- Leaflet (maps)
- Axios

## Models

- **Logistic Regression**
- **Random Forest**
- **XGBoost**
- **ResNet Style (Neural Network)**
- **Deep - Wide & Deep (Neural Network)**

## Data

Source: [Unique Registry of Victims - datos.gov.co](https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Registro-nico-de-V-ctimas-RUV-a-nivel-nacional-/dyjp-uwwh)

## Author

Fabian Luna - Universidad Nacional de Colombia

## License

This project is open source for educational and research purposes.