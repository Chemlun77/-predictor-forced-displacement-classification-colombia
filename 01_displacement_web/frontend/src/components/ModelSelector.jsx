import React from 'react';
import './ModelSelector.css';

function ModelSelector({ models, selectedModel, onModelChange }) {
  return (
    <div className="model-selector">
      <label className="label">Modelo:</label>
      <select 
        value={selectedModel} 
        onChange={(e) => onModelChange(e.target.value)}
        className="select"
      >
        <option value="">Selecciona un modelo</option>
        {models.map((model) => (
          <option key={model.name} value={model.name}>
            {model.display}
          </option>
        ))}
      </select>
    </div>
  );
}

export default ModelSelector;
