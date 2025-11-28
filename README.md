# Forced Displacement Classification Predictor - Armed Conflict in Colombia

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://displacement-predictor-frontend.onrender.com)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0-61dafb.svg)](https://reactjs.org/)
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.17-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)

Machine learning-based web application to predict and classify forced displacement events in Colombia using data from the Unique Registry of Victims (RUV). This project combines traditional ML models and deep neural networks with an AI chatbot assistant to achieve high accuracy in identifying displacement patterns from the Colombian armed conflict.

> **[📺 Watch Demo Video](https://youtube.com/...)** | **[🌐 Try Live App](https://displacement-predictor-frontend.onrender.com)**

---

## 📸 Application Features

### Main Interface
![Main Interface](docs/images/main-interface.png)
*Interactive prediction interface with real-time map visualization*

### AI Chatbot Assistant
![AI Assistant](docs/images/chatbot-demo.gif)
*Gemini-powered AI assistant explaining predictions and answering questions*

### Prediction Results
![Prediction Results](docs/images/prediction-results.png)
*Detailed prediction with validation against official RUV data*

### Interactive Map
![Interactive Map](docs/images/map-demo.gif)
*Geographic visualization showing selected department*

---

## 🌟 Key Features

- **5 Machine Learning Models:** Logistic Regression, Random Forest, XGBoost, ResNet-Style, Wide & Deep
- **AI Chatbot Assistant:** Gemini-powered explanations of predictions
- **Real-time Validation:** Compares predictions with official RUV data via API
- **Interactive Maps:** Visualize geographic patterns using Leaflet
- **7+ Million Records:** Trained on comprehensive Colombian conflict victim data
- **Professional UI:** Modern React interface with responsive design

---

## 📊 Key Results

**Best Model: Random Forest**
- **ROC-AUC:** 0.9822
- **F1-Score:** 0.8943
- **Recall:** 0.9187 (critical for humanitarian applications)
- **Training Time:** 9.54 minutes

The Random Forest model achieves near-perfect discrimination between displacement and other victimizing events, with exceptional recall ensuring minimal false negatives - crucial when dealing with humanitarian data.

---

## 📋 Project Structure
```
project_00_RUV_displacement/
├── 00_predictive_displacement_model/    # Model training and analysis
│   ├── 001_data_analysis.ipynb         # Exploratory data analysis
│   ├── 002_train_classical_model.ipynb # Classical ML training
│   ├── 003_train_neural_networks.ipynb # Deep learning training
│   ├── 004_final_report.ipynb          # Performance evaluation
│   ├── db/                              # Trained models storage
│   └── fig/                             # Visualizations and reports
└── 01_displacement_web/                 # Web application
    ├── backend/                         # Flask API
    │   ├── app.py                       # Main API endpoints
    │   ├── chatbot/                     # Gemini AI integration
    │   ├── preprocessing/               # Data cleaning
    │   ├── prediction/                  # Model inference
    │   └── api/                         # Socrata client
    ├── frontend/                        # React interface
    │   ├── src/
    │   │   ├── components/              # UI components
    │   │   └── services/                # API services
    │   └── public/
    └── db/                              # Production models
```

---

## 🤖 Models

### Training Pipeline

The project implements a comprehensive model comparison approach:

1. **Data Processing** (001_data_analysis.ipynb)
   - Dataset: 7+ million records from Colombian Unique Registry of Victims
   - Feature engineering: demographic, geographic, and temporal variables
   - Class balancing and data cleaning

2. **Classical ML Models** (002_train_classical_model.ipynb)
   - Logistic Regression
   - Random Forest
   - XGBoost
   - Grid search hyperparameter optimization
   - Cross-validation with stratified folds

3. **Neural Networks** (003_train_neural_networks.ipynb)
   - ResNet-Style architecture
   - Wide & Deep (hybrid) architecture
   - Embedding layers for categorical features
   - Early stopping and learning rate scheduling

### Performance Comparison

| Model | Training Time (min) | Accuracy Test | Precision Test | Recall Test | F1-Score Test | ROC-AUC Test |
|-------|---------------------|---------------|----------------|-------------|---------------|--------------|
| **Random Forest** | **9.54** | **0.9188** | **0.8712** | **0.9187** | **0.8943** | **0.9822** |
| XGBoost | 9.34 | 0.8629 | 0.7818 | 0.8788 | 0.8274 | 0.9510 |
| ResNet Style | 90.77 | 0.8673 | 0.9822 | 0.6572 | 0.7875 | 0.9622 |
| Deep (Wide & Deep) | 74.74 | 0.8261 | 0.9716 | 0.5512 | 0.7034 | 0.9438 |
| Logistic Regression | 48.50 | 0.7416 | 0.6305 | 0.7471 | 0.6839 | 0.8185 |

### Key Insights

- **Random Forest** achieves the best balance across all metrics with minimal training time
- **High Recall** (91.87%) ensures low false negatives - critical for humanitarian applications
- **Near-perfect ROC-AUC** (0.9822) demonstrates excellent class discrimination
- Neural networks show high precision but lower recall, suggesting they're more conservative in displacement predictions

### Features Used

The models utilize the following features:
- **Demographic:** Gender, age group (life cycle), ethnicity, disability status
- **Geographic:** Department (state), distances from Bogotá (north-south, east-west, total)
- **Temporal:** Year of occurrence (validity period)
- **Historical:** Number of previous victimizing events

---

## 🚀 Quick Start (Using Deployed App)

### Option 1: Use Live Deployment

**No installation required!** Simply visit:

🌐 **[https://displacement-predictor-frontend.onrender.com](https://displacement-predictor-frontend.onrender.com)**

**Note:** Free tier may sleep after 15 minutes of inactivity. First visit may take 30-60 seconds to wake up.

### Using the AI Chatbot

1. Make a prediction
2. Click the "AI Assistant" button (💬)
3. Provide your free Google Gemini API key:
   - Visit [ai.google.dev](https://ai.google.dev/)
   - Click "Get API key"
   - Copy and paste into the app
4. Get AI-powered explanations of predictions!

**Free tier limits:** 15 requests/minute, 1,500 requests/day

---

## 💻 Local Installation

### Option 2: Run Locally

#### Prerequisites

- **Python 3.10** (for backend)
- **Node.js 18+** (for frontend)
- **Conda** (recommended for environment management)

#### 1. Clone the repository
```bash
git clone https://github.com/Chemlun77/-predictor-forced-displacement-classification-colombia.git
cd -predictor-forced-displacement-classification-colombia
```

#### 2. Download trained models

**⚠️ Models are NOT included in the repository due to their size.**

**Download from Google Drive:**

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

#### 3. Install backend dependencies
```bash
cd 01_displacement_web/backend

# Create conda environment
conda create -n displacement python=3.10 -y
conda activate displacement

# Install dependencies
pip install -r requirements.txt
```

#### 4. Install frontend dependencies
```bash
cd ../frontend
npm install
```

#### 5. Run the application

**Terminal 1 - Backend:**
```bash
cd 01_displacement_web/backend
conda activate displacement
python app.py
```

Backend running at: **http://127.0.0.1:5000**

**Terminal 2 - Frontend:**
```bash
cd 01_displacement_web/frontend
npm start
```

Application available at: **http://localhost:3000**

---

## 🌐 Deployment Guide

Full deployment instructions available in [DEPLOYMENT.md](DEPLOYMENT.md)

### Deployment Notes

**⚠️ Random Forest Model:**
The Random Forest model (3.9 GB) is **not included in the deployment** due to Render's free tier memory limitations (512 MB). 

- **In local installation:** All 5 models available
- **In deployed version:** 4 models available (Logistic Regression, XGBoost, ResNet-Style, Deep)
- **If Random Forest is selected:** Application will display an appropriate error message

See [DEPLOYMENT.md](DEPLOYMENT.md) for details on deploying your own instance.

---

## 🔬 Training Your Own Models

To retrain the models with updated data:

### Prerequisites
```bash
# Create training environment
conda create -n model_training python=3.13 -y
conda activate model_training

# Install dependencies
pip install pandas numpy scikit-learn xgboost tensorflow matplotlib seaborn joblib openpyxl
```

### Training Steps

1. **Data Analysis** (Optional - for understanding the data)
```bash
jupyter notebook 00_predictive_displacement_model/001_data_analysis.ipynb
```

2. **Train Classical Models**
```bash
jupyter notebook 00_predictive_displacement_model/002_train_classical_model.ipynb
```
   - Downloads data automatically from datos.gov.co API
   - Trains Logistic Regression, Random Forest, and XGBoost
   - Performs grid search hyperparameter optimization
   - Saves best models to `db/02a_classical_models/saved_models/`
   - Training time: ~70 minutes total

3. **Train Neural Networks**
```bash
jupyter notebook 00_predictive_displacement_model/003_train_neural_networks.ipynb
```
   - Trains ResNet-Style and Wide & Deep architectures
   - Uses GPU if available (recommended)
   - Saves best models to `db/02b_neural_networks/saved_models/`
   - Training time: ~165 minutes total (GPU recommended)

4. **Generate Performance Report**
```bash
jupyter notebook 00_predictive_displacement_model/004_final_report.ipynb
```
   - Creates comparison tables and visualizations
   - Outputs saved to `fig/final_report/`

---

## 🔧 Technologies

**Backend:**
- Python 3.10
- Flask 3.0.0
- TensorFlow 2.17.0
- Scikit-learn 1.5.0
- XGBoost 2.1.0
- Pandas 2.2.0
- Sodapy (Socrata API)
- Google Generative AI (Gemini)

**Frontend:**
- React 18
- Leaflet (interactive maps)
- Axios (API communication)

**Training Environment:**
- Python 3.13
- Jupyter Notebooks
- GPU support for neural networks

**Deployment:**
- Render.com (hosting)
- Gunicorn (WSGI server)

---

## 🤖 AI Chatbot Features

The application includes an integrated AI assistant powered by Google's Gemini API:

### Features:
- **Automatic Explanations:** Get instant AI-generated explanations of predictions
- **Interactive Q&A:** Ask questions about the prediction, model, or results
- **Validation Context:** AI explains how predictions compare to real RUV data
- **Methodology Insights:** Learn about data processing and model decisions
- **User-Provided API Key:** Bring your own free Gemini API key (no cost to you)

### How to Use:
1. Make a prediction
2. Click the floating "💬 AI Assistant" button
3. Provide your Gemini API key (one-time setup)
4. Choose to get an automatic explanation or ask custom questions

**Get your free API key:** [ai.google.dev](https://ai.google.dev/)

---

## 📝 Data Source

**Registro Único de Víctimas (RUV) - Colombian Unique Registry of Victims**

- **Source:** [datos.gov.co](https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Registro-nico-de-V-ctimas-RUV-a-nivel-nacional-/dyjp-uwwh)
- **Records:** 7+ million victim records
- **Period:** Colombian armed conflict data
- **Update Frequency:** Regular updates from Colombian government
- **Access:** Public API via Socrata

The dataset includes information about victims of the Colombian armed conflict, categorized by type of victimizing event (forced displacement, homicide, disappearance, etc.), along with demographic and geographic information.

---

## 📄 Citation

If you use this project in your research, please cite:
```bibtex
@software{luna2025displacement,
  author = {Luna, Fabian},
  title = {Forced Displacement Classification Predictor - Armed Conflict in Colombia},
  year = {2025},
  institution = {Universidad Nacional de Colombia Sede Medellín},
  url = {https://github.com/Chemlun77/-predictor-forced-displacement-classification-colombia}
}
```

---

## 👨‍💻 Author

**Fabian Luna**  
Chemical Engineering MEng Student  
Universidad Nacional de Colombia Sede Medellín

📧 Contact: [Open an issue](https://github.com/Chemlun77/-predictor-forced-displacement-classification-colombia/issues)

---

## 📄 License

This project is open source for educational and research purposes. When using this code or models, please:

- Acknowledge the source appropriately
- Use responsibly given the sensitive humanitarian nature of the data
- Comply with datos.gov.co terms of service
- Respect victim privacy and data protection regulations

---

## 🤝 Contributing

Contributions are welcome! Areas of interest:

- Model improvements and new architectures
- Feature engineering enhancements
- Web application UI/UX improvements
- Documentation and translations
- Performance optimizations
- AI chatbot enhancements

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Ethical Considerations

This project deals with sensitive humanitarian data about victims of armed conflict. Please:

- Use the models and data responsibly
- Understand the limitations of ML predictions in humanitarian contexts
- Do not use for purposes that could harm victims or vulnerable populations
- Respect privacy and data protection principles
- Consider false negatives as more critical than false positives in this domain
- Consult with domain experts and stakeholders before production use

---

## 🐛 Known Issues & Limitations

- **Random Forest in Deployment:** Not available in free tier deployment due to size (3.9 GB)
- **Cold Starts:** Free tier deployment may take 30-60 seconds to wake from sleep
- **API Rate Limits:** Socrata API has rate limits; excessive requests may be throttled
- **Gemini API:** Requires user-provided API key; subject to Google's rate limits

---

## 📚 Additional Resources

- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Video Tutorial:** [Watch on YouTube](https://youtube.com/...)
- **Model Training Notebooks:** `00_predictive_displacement_model/`
- **API Documentation:** See `backend/app.py` for endpoint details

---

## 🙏 Acknowledgments

- **Colombian Government** for providing open data through datos.gov.co
- **Universidad Nacional de Colombia** for academic support
- **Victims of the Colombian Armed Conflict** whose data helps understand and prevent future humanitarian crises

---

**Note:** This is an academic project for research and educational purposes. Production deployment for humanitarian applications should include additional validation, ethical review, and stakeholder consultation.

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**