import React, { useState, useEffect } from 'react';
import ControlPanel from './components/ControlPanel';
import MapView from './components/MapView';
import Chatbot from './components/Chatbot';
import { getModels, getVariables, getDepartments } from './services/apiService';
import './App.css';

function App() {
  const [models, setModels] = useState([]);
  const [variables, setVariables] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Chatbot state
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatbotContext, setChatbotContext] = useState(null);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [modelsRes, variablesRes, deptsRes] = await Promise.all([
          getModels(),
          getVariables(),
          getDepartments()
        ]);
        
        setModels(modelsRes.data.models);
        setVariables(variablesRes.data);
        setDepartments(deptsRes.data.departments);
        setLoading(false);
      } catch (error) {
        console.error('Error loading initial data:', error);
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  const [hasAutoOpened, setHasAutoOpened] = useState(false);

  // Update chatbot context when prediction changes
  useEffect(() => {
    if (predictionResult && predictionResult.userInput) {
      const newPredictionId = JSON.stringify(predictionResult.userInput);
      
      setChatbotContext({
        userInput: predictionResult.userInput,
        prediction: {
          model: predictionResult.model,
          prediction: predictionResult.prediction,
          confidence: predictionResult.confidence,
          label: predictionResult.label,
          match_type: predictionResult.match_type,
          real_label: predictionResult.real_label,
          is_correct: predictionResult.is_correct,
          displacement_count: predictionResult.displacement_count,
          other_count: predictionResult.other_count,
          matches_data: predictionResult.matches_data
        },
        modelMetrics: getModelMetrics(predictionResult.model)
      });
      
      // Auto-open chatbot ONLY on NEW prediction, NOT when user closes it
      if (!hasAutoOpened) {
        setShowChatbot(true);
        setHasAutoOpened(true);
      }
    }
  }, [predictionResult]);

// Reset auto-open flag when chatbot is manually closed
useEffect(() => {
  if (!showChatbot) {
    setHasAutoOpened(false);
  }
}, [showChatbot]);

  const getModelMetrics = (modelName) => {
    const metrics = {
      'Logistic_Regression': {
        accuracy: 0.7416,
        precision: 0.6305,
        recall: 0.7471,
        f1_score: 0.6839,
        roc_auc: 0.8185
      },
      'Random_Forest': {
        accuracy: 0.9188,
        precision: 0.8712,
        recall: 0.9187,
        f1_score: 0.8943,
        roc_auc: 0.9822
      },
      'XGBoost': {
        accuracy: 0.8629,
        precision: 0.7818,
        recall: 0.8788,
        f1_score: 0.8274,
        roc_auc: 0.9510
      },
      'ResNet_Style': {
        accuracy: 0.8673,
        precision: 0.9822,
        recall: 0.6572,
        f1_score: 0.7875,
        roc_auc: 0.9622
      },
      'Deep': {
        accuracy: 0.8261,
        precision: 0.9716,
        recall: 0.5512,
        f1_score: 0.7034,
        roc_auc: 0.9438
      }
    };
    
    return metrics[modelName] || {};
  };

  const handlePredictionResult = (result) => {
    setPredictionResult(result);
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '20px'
      }}>
        Cargando aplicación...
      </div>
    );
  }

  return (
    <div className="app">
      <header className={`app-header ${showChatbot ? 'with-chatbot' : ''}`}>
        <img 
          src="/logo_app.png" 
          alt="V-DataLab Logo" 
          style={{
            width: '160px',
            height: '80px',
            borderRadius: '10px',
            marginRight: '20px'
          }}
        />
        <h1>Laboratorio de Aprendizaje con IA sobre Desplazamiento Forzado en Colombia</h1>
      </header>
      <div className={`app-content ${showChatbot ? 'with-chatbot' : ''}`}>
        <ControlPanel
          models={models}
          variables={variables}
          departments={departments}
          onDepartmentChange={setSelectedDepartment}
          onPredictionResult={handlePredictionResult}
        />
        <MapView
          departments={departments}
          selectedDepartment={selectedDepartment}
        />
      </div>

      {/* Floating chat button */}
      {!showChatbot && (
        <button 
          className="floating-chat-btn"
          onClick={() => setShowChatbot(true)}
          title="Open AI Assistant"
        >
          <span className="chat-icon">💬</span>
          <span className="chat-label">Asistente de IA</span>
        </button>
      )}

      {/* Chatbot component */}
      <Chatbot
        predictionContext={chatbotContext}
        isVisible={showChatbot}
        onToggle={() => setShowChatbot(false)}
      />
    </div>
  );
}

export default App;
