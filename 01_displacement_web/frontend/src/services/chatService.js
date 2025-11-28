/**
 * Chat Service - API communication for chatbot
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api/chat`
  : 'http://127.0.0.1:5000/api/chat';

/**
 * Test if Gemini API key is valid
 */
export const testApiKey = async (apiKey) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/test-key`, {
      api_key: apiKey
    });
    return response.data;
  } catch (error) {
    console.error('Error testing API key:', error);
    throw error;
  }
};

/**
 * Get AI explanation for a prediction
 */
export const getExplanation = async (apiKey, userInput, prediction, modelName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/explain`, {
      api_key: apiKey,
      user_input: userInput,
      prediction: prediction,
      model_name: modelName
    });
    
    // ✅ CORRECCIÓN: Extraer solo el texto de la explicación
    if (response.data && response.data.success) {
      return response.data.explanation;
    } else {
      throw new Error(response.data.error || 'Failed to get explanation');
    }
  } catch (error) {
    console.error('Error getting explanation:', error);
    throw error;
  }
};

/**
 * Send a chat message with context
 */
export const sendChatMessage = async (apiKey, message, context, conversationHistory = []) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/message`, {
      api_key: apiKey,
      message: message,
      context: context,
      conversation_history: conversationHistory
    });
    
    // ✅ CORRECCIÓN: Extraer solo el texto de la respuesta
    if (response.data && response.data.success) {
      return response.data.response;
    } else {
      throw new Error(response.data.error || 'Failed to get response');
    }
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};