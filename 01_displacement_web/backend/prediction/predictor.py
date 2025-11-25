import joblib
import numpy as np
import pandas as pd
import keras
import os
import tensorflow as tf

@keras.saving.register_keras_serializable()
def focal_loss_fixed(gamma=2.0, alpha=0.25):
    def focal_loss_fn(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
        
        y_true = tf.cast(y_true, tf.float32)
        
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = alpha * y_true * tf.pow(1 - y_pred, gamma)
        
        loss = weight * cross_entropy
        return tf.reduce_mean(loss)
    
    return focal_loss_fn

class ModelPredictor:
    def __init__(self, models_dir='../db'):
        self.models_dir = models_dir
        self.models = {}
        self.encoders = {}
        self.scalers = {}
        self.load_models()
    
    def load_models(self):
        classic_path = os.path.join(self.models_dir, '02a_classical_models/saved_models')
        nn_path = os.path.join(self.models_dir, '02b_neural_networks/saved_models')
        
        try:
            self.models['Logistic_Regression'] = joblib.load(
                os.path.join(classic_path, 'Logistic_Regression_best_model.pkl'))
            self.models['Random_Forest'] = joblib.load(
                os.path.join(classic_path, 'Random_Forest_best_model.pkl'))
            self.models['XGBoost'] = joblib.load(
                os.path.join(classic_path, 'XGBoost_best_model.pkl'))
            
            self.encoders['classic'] = joblib.load(
                os.path.join(classic_path, 'categorical_encoders.pkl'))
            self.scalers['classic'] = joblib.load(
                os.path.join(classic_path, 'numeric_scalers.pkl'))
            
            self.models['ResNet_Style'] = keras.models.load_model(
                os.path.join(nn_path, 'ResNet_Style_best_model.keras'))
            self.models['Deep'] = keras.models.load_model(
                os.path.join(nn_path, 'Deep_best_model.keras'))
            
            self.encoders['nn'] = joblib.load(
                os.path.join(nn_path, 'categorical_encoders.pkl'))
            self.scalers['nn'] = joblib.load(
                os.path.join(nn_path, 'numeric_scalers.pkl'))
            self.embedding_info = joblib.load(
                os.path.join(nn_path, 'embedding_info.pkl'))
            
            print("✓ All models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def preprocess_classic(self, input_data):
        categorical_cols = ['SEXO', 'ETNIA', 'CICLO_VITAL', 'DISCAPACIDAD', 'ESTADO_DEPTO']
        numeric_cols = ['EVENTOS', 'VIGENCIA', 'km_norte_sur', 'km_este_oeste', 'distancia_total']
        
        X_cat_parts = []
        encoders = self.encoders['classic']
        
        if 'onehot' in encoders:
            enc = encoders['onehot']
            onehot_cols = [col for col in categorical_cols if col in enc.feature_names_in_]
            if onehot_cols:
                X_cat_encoded = enc.transform([[input_data[col] for col in onehot_cols]])
                X_cat_parts.append(pd.DataFrame(X_cat_encoded, columns=enc.get_feature_names_out()))
        
        if 'ordinal' in encoders:
            enc = encoders['ordinal']
            ordinal_cols = [col for col in categorical_cols if col in enc.feature_names_in_]
            if ordinal_cols:
                X_cat_encoded = enc.transform([[input_data[col] for col in ordinal_cols]])
                X_cat_parts.append(pd.DataFrame(X_cat_encoded, columns=ordinal_cols))
        
        if X_cat_parts:
            X_categorical = pd.concat(X_cat_parts, axis=1)
        else:
            X_categorical = pd.DataFrame()
        
        X_numeric = pd.DataFrame([[input_data[col] for col in numeric_cols]], columns=numeric_cols)
        
        for col in numeric_cols:
            if col in self.scalers['classic']:
                scaler = self.scalers['classic'][col]
                X_numeric[col] = scaler.transform(X_numeric[[col]])
        
        X = pd.concat([X_categorical, X_numeric], axis=1)
        
        return X
    
    def preprocess_nn(self, input_data):
        categorical_cols = ['SEXO', 'ETNIA', 'CICLO_VITAL', 'DISCAPACIDAD', 'ESTADO_DEPTO']
        numeric_cols = ['EVENTOS', 'VIGENCIA', 'km_norte_sur', 'km_este_oeste', 'distancia_total']
        
        X_cat = {}
        encoders = self.encoders['nn']
        
        for col in categorical_cols:
            if col in encoders:
                enc = encoders[col]
                value = [[input_data[col]]]
                encoded = enc.transform(value).astype('int32').flatten()[0]
                X_cat[col] = np.array([encoded])
        
        X_num = np.array([[input_data[col] for col in numeric_cols]], dtype='float32')
        
        for idx, col in enumerate(numeric_cols):
            if col in self.scalers['nn']:
                scaler = self.scalers['nn'][col]
                X_num[:, idx] = scaler.transform(X_num[:, [idx]]).flatten()
        
        inputs = list(X_cat.values()) + [X_num]
        
        return inputs
    
    def predict(self, model_name, input_data):
        model = self.models.get(model_name)
        
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        if model_name in ['Logistic_Regression', 'Random_Forest', 'XGBoost']:
            X = self.preprocess_classic(input_data)
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)[0][1]
            else:
                proba = float(model.predict(X)[0])
            
            pred = 1 if proba >= 0.5 else 0
            
        else:
            X = self.preprocess_nn(input_data)
            proba = float(model.predict(X, verbose=0)[0][0])
            pred = 1 if proba >= 0.5 else 0
        
        return {
            'prediction': int(pred),
            'probability': float(proba)
        }
