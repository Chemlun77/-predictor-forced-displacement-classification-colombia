import React from 'react';
import './VariableInputs.css';

// Training data ranges
const TRAINING_RANGES = {
  VIGENCIA: { min: 1985, max: 2025 },
  EVENTOS: { min: 0, max: 351905 }
};

function VariableInputs({ variables, departments, values, onChange }) {
  if (!variables) return null;

  // Check if values are out of range
  const isVigenciaOutOfRange = values.VIGENCIA && (
    parseInt(values.VIGENCIA) < TRAINING_RANGES.VIGENCIA.min || 
    parseInt(values.VIGENCIA) > TRAINING_RANGES.VIGENCIA.max
  );

  const isEventosOutOfRange = values.EVENTOS !== '' && (
    parseInt(values.EVENTOS) < TRAINING_RANGES.EVENTOS.min || 
    parseInt(values.EVENTOS) > TRAINING_RANGES.EVENTOS.max
  );

  return (
    <div className="variable-inputs">
      <h3 className="section-title">Variables Predictoras</h3>
      
      <div className="input-group">
        <label className="label">Departamento:</label>
        <select 
          value={values.ESTADO_DEPTO} 
          onChange={(e) => onChange('ESTADO_DEPTO', e.target.value)}
          className="select"
        >
          <option value="">Selecciona departamento</option>
          {variables.categorical.ESTADO_DEPTO.map((dept) => (
            <option key={dept} value={dept}>{dept}</option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label className="label">Sexo:</label>
        <select 
          value={values.SEXO} 
          onChange={(e) => onChange('SEXO', e.target.value)}
          className="select"
        >
          <option value="">Selecciona sexo</option>
          {variables.categorical.SEXO.map((sex) => (
            <option key={sex} value={sex}>{sex}</option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label className="label">Etnia:</label>
        <select 
          value={values.ETNIA} 
          onChange={(e) => onChange('ETNIA', e.target.value)}
          className="select"
        >
          <option value="">Selecciona etnia</option>
          {variables.categorical.ETNIA.map((etnia) => (
            <option key={etnia} value={etnia}>{etnia}</option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label className="label">Discapacidad:</label>
        <select 
          value={values.DISCAPACIDAD} 
          onChange={(e) => onChange('DISCAPACIDAD', e.target.value)}
          className="select"
        >
          <option value="">Selecciona discapacidad</option>
          {variables.categorical.DISCAPACIDAD.map((disc) => (
            <option key={disc} value={disc}>{disc}</option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label className="label">Ciclo Vital:</label>
        <select 
          value={values.CICLO_VITAL} 
          onChange={(e) => onChange('CICLO_VITAL', e.target.value)}
          className="select"
        >
          <option value="">Selecciona ciclo vital</option>
          {variables.categorical.CICLO_VITAL.map((ciclo) => (
            <option key={ciclo} value={ciclo}>{ciclo}</option>
          ))}
        </select>
      </div>

      <div className="input-group">
        <label className="label">Año (VIGENCIA):</label>
        <input 
          type="number"
          value={values.VIGENCIA}
          onChange={(e) => onChange('VIGENCIA', e.target.value)}
          className="input"
        />
        {isVigenciaOutOfRange && (
          <div className="input-warning">
            ⚠ Año fuera del rango de entrenamiento ({TRAINING_RANGES.VIGENCIA.min}-{TRAINING_RANGES.VIGENCIA.max}). 
            La predicción puede ser menos confiable.
          </div>
        )}
      </div>

      <div className="input-group">
        <label className="label">Eventos:</label>
        <input 
          type="number"
          value={values.EVENTOS}
          onChange={(e) => onChange('EVENTOS', e.target.value)}
          className="input"
        />
        {isEventosOutOfRange && (
          <div className="input-warning">
            ⚠ Eventos fuera del rango de entrenamiento ({TRAINING_RANGES.EVENTOS.min.toLocaleString()}-{TRAINING_RANGES.EVENTOS.max.toLocaleString()}). 
            La predicción puede ser menos confiable.
          </div>
        )}
      </div>

      <h3 className="section-title">Variables Geográficas (Automáticas)</h3>

      <div className="input-group">
        <label className="label">km Norte-Sur:</label>
        <input 
          type="text"
          value={values.km_norte_sur}
          readOnly
          className="input readonly"
        />
      </div>

      <div className="input-group">
        <label className="label">km Este-Oeste:</label>
        <input 
          type="text"
          value={values.km_este_oeste}
          readOnly
          className="input readonly"
        />
      </div>

      <div className="input-group">
        <label className="label">Distancia Total (km):</label>
        <input 
          type="text"
          value={values.distancia_total}
          readOnly
          className="input readonly"
        />
      </div>
    </div>
  );
}

export default VariableInputs;
