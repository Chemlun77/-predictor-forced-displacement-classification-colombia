import React, { useState, useEffect } from 'react';
import ModelSelector from './ModelSelector';
import VariableInputs from './VariableInputs';
import PredictionResult from './PredictionResult';
import { predict, getDepartmentGeo, getRandomValues } from '../services/apiService';
import './ControlPanel.css';

function ControlPanel({ models, variables, departments, onDepartmentChange, onPredictionResult }) {
  const [selectedModel, setSelectedModel] = useState('');
  const [formValues, setFormValues] = useState({
    ESTADO_DEPTO: '',
    SEXO: '',
    ETNIA: '',
    DISCAPACIDAD: '',
    CICLO_VITAL: '',
    VIGENCIA: '',
    EVENTOS: '',
    km_norte_sur: '',
    km_este_oeste: '',
    distancia_total: ''
  });
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDepartmentChange = async (deptName) => {
    setFormValues(prev => ({ ...prev, ESTADO_DEPTO: deptName }));
    onDepartmentChange(deptName);
    
    if (deptName) {
      try {
        const response = await getDepartmentGeo(deptName);
        const { km_norte_sur, km_este_oeste, distancia_total } = response.data;
        setFormValues(prev => ({
          ...prev,
          km_norte_sur,
          km_este_oeste,
          distancia_total
        }));
      } catch (error) {
        console.error('Error fetching department geo:', error);
      }
    }
  };

  const handleInputChange = (name, value) => {
    if (name === 'ESTADO_DEPTO') {
      handleDepartmentChange(value);
    } else {
      setFormValues(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleRandomValues = async () => {
    try {
      const response = await getRandomValues();
      const randomData = response.data;
      setFormValues(randomData);
      onDepartmentChange(randomData.ESTADO_DEPTO);
    } catch (error) {
      console.error('Error getting random values:', error);
    }
  };

  const handlePredict = async () => {
    if (!selectedModel) {
      alert('Por favor selecciona un modelo');
      return;
    }

    const requiredFields = ['ESTADO_DEPTO', 'SEXO', 'ETNIA', 'DISCAPACIDAD', 'CICLO_VITAL', 'VIGENCIA', 'EVENTOS'];
    const missingFields = requiredFields.filter(field => !formValues[field]);
    
    if (missingFields.length > 0) {
      alert(`Por favor completa los siguientes campos: ${missingFields.join(', ')}`);
      return;
    }

    setLoading(true);
    try {
      const response = await predict({
        model: selectedModel,
        ...formValues
      });
      
      setPredictionResult(response.data);
      onPredictionResult(response.data);
    } catch (error) {
      console.error('Error making prediction:', error);
      alert('Error al realizar la predicción');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="control-panel">
      <div className="control-panel-content">
        <ModelSelector
          models={models}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
        />
        
        <VariableInputs
          variables={variables}
          departments={departments}
          values={formValues}
          onChange={handleInputChange}
        />
        
        <div className="button-group">
          <button onClick={handleRandomValues} className="btn btn-secondary">
            Valores Aleatorios
          </button>
          <button onClick={handlePredict} className="btn btn-primary" disabled={loading}>
            {loading ? 'Prediciendo...' : 'Predecir'}
          </button>
        </div>

        {predictionResult && (
          <PredictionResult result={predictionResult} />
        )}
      </div>
    </div>
  );
}

export default ControlPanel;
