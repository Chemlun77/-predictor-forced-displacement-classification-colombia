import React, { useState } from 'react';
import './ApiKeyModal.css';

const ApiKeyModal = ({ isOpen, onClose, onSubmit, isLoading }) => {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!apiKey.trim()) {
      setError('API key is required');
      return;
    }
    
    if (!apiKey.startsWith('AIza')) {
      setError('Invalid API key format. Gemini keys start with "AIza"');
      return;
    }
    
    setError('');
    onSubmit(apiKey);
  };

  const handleClose = () => {
    setApiKey('');
    setError('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="api-key-modal-overlay">
      <div className="api-key-modal">
        <div className="modal-header">
          <h2>🤖 Asistente de chat con IA</h2>
          <button className="close-btn" onClick={handleClose}>×</button>
        </div>

        <div className="modal-body">
          <p className="modal-description">
            Para utilizar el asistente de chat con IA, necesitas una API key gratuita de Google Gemini.
          </p>

          <div className="info-box">
            <p><strong>¿Cómo obtener tu clave API gratuita?:</strong></p>
            <ol>
              <li>Ir a <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">ai.google.dev</a></li>
              <li>Haga clic en «Obtener API key en Google AI Studio».</li>
              <li>Sign in with your Google account</li>
              <li>Inicie sesión con su cuenta de Google.</li>
              <li>Copia tu clave y pégala a continuación.</li>
            </ol>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="apiKey">Introduzca su API key:</label>
              <input
                type="password"
                id="apiKey"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="AIza..."
                className={error ? 'error' : ''}
                disabled={isLoading}
              />
              {error && <span className="error-message">{error}</span>}
            </div>

            <div className="security-note">
              <small>
                🔒 Tu API key se almacena únicamente en tu navegador (localStorage) y nunca se comparte con nuestros servidores.
                Cada solicitud se realiza directamente a la API Gemini de Google utilizando su clave.
              </small>
            </div>

            <div className="modal-actions">
              <button 
                type="button" 
                onClick={handleClose} 
                className="btn-cancel"
                disabled={isLoading}
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                className="btn-submit"
                disabled={isLoading}
              >
                {isLoading ? 'Validando...' : 'Guardar e iniciar chat'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ApiKeyModal;
