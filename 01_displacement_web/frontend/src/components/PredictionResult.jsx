import React from 'react';
import './PredictionResult.css';

function PredictionResult({ result }) {
  if (!result) return null;

  const predictionLabel = result.prediction === 1 
    ? 'Desplazamiento Forzado' 
    : 'Otro Hecho Victimizante';

  return (
    <div className="prediction-result">
      <h3 className="result-title">Resultado de Predicción</h3>
      
      <div className="result-box">
        <div className="result-item">
          <strong>Predicción del modelo:</strong>
          <span className={`result-badge ${result.prediction === 1 ? 'displacement' : 'other'}`}>
            {predictionLabel}
          </span>
        </div>

        {result.match_type === 'no_match' && (
          <div className="validation-info warning">
            <p><strong>{result.message}</strong></p>
            <p>{result.submessage}</p>
          </div>
        )}

        {result.match_type === 'exact_match' && (
          <div className="validation-info success">
            <p><strong>{result.message}</strong></p>
            <div className="result-item">
              <strong>Valor real:</strong>
              <span className={`result-badge ${result.real_value === 1 ? 'displacement' : 'other'}`}>
                {result.real_label}
              </span>
            </div>
            <div className="result-item">
              <strong>Resultado:</strong>
              <span className={`result-status ${result.is_correct ? 'correct' : 'incorrect'}`}>
                {result.is_correct ? '✓ CORRECTO' : '✗ INCORRECTO'}
              </span>
            </div>
          </div>
        )}

        {result.match_type === 'ambiguous' && (
          <div className="validation-info warning">
            <p><strong>{result.message}</strong></p>
            <ul>
              <li>{result.displacement_count} casos: Desplazamiento Forzado</li>
              <li>{result.other_count} casos: Otro Hecho Victimizante</li>
            </ul>
            <p className="note"><em>{result.submessage}</em></p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PredictionResult;
