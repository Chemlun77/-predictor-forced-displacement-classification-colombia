import React, { useState, useEffect, useRef } from 'react';
import ApiKeyModal from './ApiKeyModal';
import { testApiKey, getExplanation, sendChatMessage } from '../services/chatService';
import './Chatbot.css';

function Chatbot({ predictionContext, isVisible, onToggle }) {
  const [apiKey, setApiKey] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isValidatingKey, setIsValidatingKey] = useState(false);
  const [showExplanationPrompt, setShowExplanationPrompt] = useState(false);
  const lastPredictionRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Load API key from localStorage on mount
  useEffect(() => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
      setApiKey(savedKey);
    }
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Show explanation prompt ONLY when prediction CHANGES (not on every render)
  useEffect(() => {
    if (predictionContext && apiKey) {
      const currentPrediction = JSON.stringify(predictionContext);
      if (currentPrediction !== lastPredictionRef.current) {
        lastPredictionRef.current = currentPrediction;
        setMessages([]);
        setShowExplanationPrompt(true);
      }
    }
  }, [predictionContext, apiKey]);

  const handleApiKeySubmit = async (key) => {
    setIsValidatingKey(true);
    try {
      const response = await testApiKey(key);
      
      if (response.success) {
        setApiKey(key);
        localStorage.setItem('gemini_api_key', key);
        setShowModal(false);
        
        if (predictionContext && messages.length === 0) {
          setShowExplanationPrompt(true);
        }
      } else {
        alert(response.message || 'Invalid API key');
      }
    } catch (error) {
      alert('Error validating API key: ' + error.message);
    } finally {
      setIsValidatingKey(false);
    }
  };

  const handleGenerateExplanation = async () => {
    if (!predictionContext || !apiKey) return;

    setShowExplanationPrompt(false);
    setIsLoading(true);
    
    const systemMessage = {
      role: 'system',
      content: 'Generando explicación automática...',
      timestamp: new Date().toISOString()
    };
    setMessages([systemMessage]);

    try {
      const explanation = await getExplanation(
        apiKey,
        predictionContext.userInput,
        predictionContext.prediction,
        predictionContext.prediction.model
      );

      setMessages([{
        role: 'assistant',
        content: explanation,
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      setMessages([{
        role: 'system',
        content: 'Error generando explicación. Por favor verifica tu API key o intenta de nuevo.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkipExplanation = () => {
    setShowExplanationPrompt(false);
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || !apiKey || !predictionContext) return;

    if (showExplanationPrompt) {
      setShowExplanationPrompt(false);
    }

    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(
        apiKey,
        messageText,
        {
          userInput: predictionContext.userInput,
          prediction: predictionContext.prediction,
          modelMetrics: predictionContext.modelMetrics
        },
        messages
      );

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'system',
        content: 'Error: ' + error.message,
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setShowExplanationPrompt(true);
  };

  const handleChangeApiKey = () => {
    setShowModal(true);
  };

  const handleRemoveApiKey = () => {
    if (window.confirm('¿Estás seguro de que deseas eliminar la API key?')) {
      setApiKey('');
      localStorage.removeItem('gemini_api_key');
      setMessages([]);
      setShowExplanationPrompt(false);
    }
  };

  if (!isVisible) return null;

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-left">
          <span className="chatbot-icon">🤖</span>
          <h3>AI Assistant</h3>
        </div>
        <div className="header-actions">
          {messages.length > 0 && (
            <button 
              className="icon-btn" 
              onClick={handleClearChat} 
              title="Clear chat"
            >
              🗑️
            </button>
          )}
          <button 
            className="icon-btn" 
            onClick={onToggle}
            title="Close"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="chatbot-body">
        {!apiKey ? (
          <div className="no-api-key">
            <div className="setup-message">
              <h4>🔑 Setup Required</h4>
              <p>To use the AI Assistant, you need to provide your Google Gemini API key.</p>
              <button className="btn-primary" onClick={() => setShowModal(true)}>
                Setup API Key
              </button>
              <div className="api-key-info">
                <small>
                  <strong>How to get your free API key:</strong><br/>
                  1. Visit <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">ai.google.dev</a><br/>
                  2. Click "Get API key"<br/>
                  3. Create a new API key<br/>
                  4. Copy and paste it here<br/><br/>
                  <strong>Free tier:</strong> 15 requests/minute, 1,500 requests/day
                </small>
              </div>
            </div>
          </div>
        ) : !predictionContext ? (
          <div className="no-prediction">
            <p>📊</p>
            <p>Haz una predicción para comenzar a chatear con el asistente de IA</p>
          </div>
        ) : (
          <div className="messages-container">
            {showExplanationPrompt && (
              <div className="explanation-prompt">
                <p>🤖 ¿Quieres que explique la predicción que acabas de hacer?</p>
                <div className="prompt-buttons">
                  <button 
                    className="btn-primary" 
                    onClick={handleGenerateExplanation}
                    disabled={isLoading}
                  >
                    Sí, explícame
                  </button>
                  <button 
                    className="btn-secondary" 
                    onClick={handleSkipExplanation}
                    disabled={isLoading}
                  >
                    No, solo quiero chatear
                  </button>
                </div>
              </div>
            )}

            {!showExplanationPrompt && messages.length === 0 && !isLoading && (
              <div className="welcome-message">
                <p>Pregúntame lo que quieras sobre esta predicción</p>
                <div className="suggested-questions">
                  <small>Preguntas sugeridas:</small>
                  <button onClick={() => handleSendMessage("¿Por qué esta predicción?")}>
                    ¿Por qué esta predicción?
                  </button>
                  <button onClick={() => handleSendMessage("¿Cuáles son los factores clave?")}>
                    ¿Cuáles son los factores clave?
                  </button>
                  <button onClick={() => handleSendMessage("Explícame la predicción")}>
                    Explícame la predicción
                  </button>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                </div>
                <div className="message-timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message loading">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="chatbot-footer">
        <form 
          className="message-form" 
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage(inputMessage);
          }}
        >
          <input
            type="text"
            className="message-input"
            placeholder={predictionContext ? "Pregúntame lo que quieras..." : "Haz una predicción primero"}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={!predictionContext || !apiKey || isLoading}
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!inputMessage.trim() || !predictionContext || !apiKey || isLoading}
          >
            ➤
          </button>
        </form>

        <div className="footer-actions">
          <button className="text-btn" onClick={handleChangeApiKey}>
            Cambiar API Key
          </button>
          <span className="separator">•</span>
          <button className="text-btn" onClick={handleRemoveApiKey}>
            Eliminar API Key
          </button>
        </div>
      </div>

      <ApiKeyModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onSubmit={handleApiKeySubmit}
        isLoading={isValidatingKey}
      />
    </div>
  );
}

export default Chatbot;