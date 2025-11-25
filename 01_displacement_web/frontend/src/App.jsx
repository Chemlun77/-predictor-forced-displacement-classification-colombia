import React, { useState, useEffect } from 'react';
import ControlPanel from './components/ControlPanel';
import MapView from './components/MapView';
import { getModels, getVariables, getDepartments } from './services/apiService';
import './App.css';

function App() {
  const [models, setModels] = useState([]);
  const [variables, setVariables] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(true);

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
      <header className="app-header">
        <h1>Predictor de Clasificación de Desplazamiento Forzado - Conflicto Armado en Colombia</h1>
      </header>
      <div className="app-content">
        <ControlPanel
          models={models}
          variables={variables}
          departments={departments}
          onDepartmentChange={setSelectedDepartment}
          onPredictionResult={setPredictionResult}
        />
        <MapView
          departments={departments}
          selectedDepartment={selectedDepartment}
        />
      </div>
    </div>
  );
}

export default App;
