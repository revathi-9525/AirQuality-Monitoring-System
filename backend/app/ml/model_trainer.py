import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from datetime import datetime
from .feature_engineering import create_features, prepare_training_data

class ModelTrainer:
    def __init__(self):
        self.models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'xgboost': XGBRegressor(n_estimators=100, random_state=42)
        }
        self.best_model = None
        self.best_model_name = None
        self.metrics = {}
    
    def train_models(self, df: pd.DataFrame):
        df_features = create_features(df)
        X, y = prepare_training_data(df_features)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        best_score = -np.inf
        
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            self.metrics[name] = {
                'mae': float(mae),
                'rmse': float(rmse),
                'r2': float(r2)
            }
            
            if r2 > best_score:
                best_score = r2
                self.best_model = model
                self.best_model_name = name
        
        return self.metrics
    
    def save_model(self, path: str = "backend/trained_models"):
        os.makedirs(path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"{path}/best_model_{self.best_model_name}_{timestamp}.pkl"
        joblib.dump(self.best_model, model_path)
        
        metadata_path = f"{path}/model_metadata.pkl"
        joblib.dump({
            'model_name': self.best_model_name,
            'metrics': self.metrics,
            'timestamp': timestamp
        }, metadata_path)
        
        return model_path
    
    def load_model(self, path: str = "backend/trained_models/model_metadata.pkl"):
        if os.path.exists(path):
            metadata = joblib.load(path)
            model_files = [f for f in os.listdir("backend/trained_models") if f.startswith("best_model")]
            if model_files:
                latest_model = sorted(model_files)[-1]
                self.best_model = joblib.load(f"backend/trained_models/{latest_model}")
                self.best_model_name = metadata['model_name']
                self.metrics = metadata['metrics']
                return True
        return False
    
    def predict(self, features: pd.DataFrame):
        if self.best_model is None:
            raise ValueError("No model loaded")
        return self.best_model.predict(features)
