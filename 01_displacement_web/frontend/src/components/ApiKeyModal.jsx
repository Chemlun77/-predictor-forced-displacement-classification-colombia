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
          <h2>🤖 AI Chat Assistant</h2>
          <button className="close-btn" onClick={handleClose}>×</button>
        </div>

        <div className="modal-body">
          <p className="modal-description">
            To use the AI chat assistant, you need a free Google Gemini API key.
          </p>

          <div className="info-box">
            <p><strong>How to get your free API key:</strong></p>
            <ol>
              <li>Go to <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">ai.google.dev</a></li>
              <li>Click "Get API key in Google AI Studio"</li>
              <li>Sign in with your Google account</li>
              <li>Click "Get API key" → "Create API key"</li>
              <li>Copy your key and paste it below</li>
            </ol>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="apiKey">Enter your API key:</label>
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
                🔒 Your API key is stored only in your browser (localStorage) and never shared with our servers.
                Each request is made directly to Google's Gemini API using your key.
              </small>
            </div>

            <div className="modal-actions">
              <button 
                type="button" 
                onClick={handleClose} 
                className="btn-cancel"
                disabled={isLoading}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="btn-submit"
                disabled={isLoading}
              >
                {isLoading ? 'Validating...' : 'Save & Start Chat'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ApiKeyModal;
