# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy import desc
# import pandas as pd
# from datetime import datetime, timedelta
# from ..database import get_db
# from ..models import City, AirQualityData, Prediction
# from ..ml.model_trainer import ModelTrainer
# from ..ml.feature_engineering import create_features
# from pydantic import BaseModel

# router = APIRouter(prefix="/api", tags=["ml"])

# trainer = ModelTrainer()

# class TrainResponse(BaseModel):
#     message: str
#     metrics: dict

# class PredictionResponse(BaseModel):
#     city_name: str
#     current_aqi: float
#     predicted_aqi: float
#     prediction_time: datetime
#     model_version: str

# @router.post("/train-model", response_model=TrainResponse)
# def train_model(city_name: str, db: Session = Depends(get_db)):
#     city = db.query(City).filter(City.name == city_name).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="City not found")
    
#     aqi_data = db.query(AirQualityData).filter(
#         AirQualityData.city_id == city.id
#     ).order_by(AirQualityData.timestamp).all()
    
#     if len(aqi_data) < 50:
#         raise HTTPException(status_code=400, detail="Insufficient data for training (minimum 50 records)")
    
#     df = pd.DataFrame([{
#         'timestamp': record.timestamp,
#         'pm2_5': record.pm2_5,
#         'pm10': record.pm10,
#         'no2': record.no2,
#         'so2': record.so2,
#         'co': record.co,
#         'o3': record.o3,
#         'aqi': record.aqi
#     } for record in aqi_data])
    
#     metrics = trainer.train_models(df)
#     model_path = trainer.save_model()
    
#     return {
#         "message": f"Model trained successfully. Best model: {trainer.best_model_name}",
#         "metrics": metrics
#     }

# @router.get("/predict/{city_name}", response_model=PredictionResponse)
# def predict_aqi(city_name: str, db: Session = Depends(get_db)):
#     city = db.query(City).filter(City.name == city_name).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="City not found")
    
#     if trainer.best_model is None:
#         trainer.load_model()
    
#     if trainer.best_model is None:
#         raise HTTPException(status_code=400, detail="No trained model available")
    
#     recent_data = db.query(AirQualityData).filter(
#         AirQualityData.city_id == city.id
#     ).order_by(desc(AirQualityData.timestamp)).limit(24).all()
    
#     if len(recent_data) < 3:
#         raise HTTPException(status_code=400, detail="Insufficient recent data for prediction")
    
#     df = pd.DataFrame([{
#         'timestamp': record.timestamp,
#         'pm2_5': record.pm2_5,
#         'pm10': record.pm10,
#         'no2': record.no2,
#         'so2': record.so2,
#         'co': record.co,
#         'o3': record.o3,
#         'aqi': record.aqi
#     } for record in reversed(recent_data)])
    
#     df_features = create_features(df)
    
#     if len(df_features) == 0:
#         raise HTTPException(status_code=400, detail="Unable to create features")
    
#     latest_features = df_features.iloc[-1:][['pm2_5', 'pm10', 'no2', 'so2', 'co', 'o3',
#                                               'aqi_lag_1', 'aqi_lag_2', 'aqi_lag_3',
#                                               'aqi_rolling_24h', 'aqi_delta',
#                                               'hour', 'day_of_week', 'month', 'pm_ratio']]
    
#     predicted_aqi = trainer.predict(latest_features)[0]
#     prediction_time = datetime.utcnow() + timedelta(hours=1)
    
#     prediction = Prediction(
#         city_id=city.id,
#         predicted_aqi=float(predicted_aqi),
#         prediction_time=prediction_time,
#         model_version=trainer.best_model_name
#     )
#     db.add(prediction)
#     db.commit()
    
#     return {
#         "city_name": city_name,
#         "current_aqi": float(recent_data[0].aqi),
#         "predicted_aqi": float(predicted_aqi),
#         "prediction_time": prediction_time,
#         "model_version": trainer.best_model_name
#     }

# @router.get("/model-metrics")
# def get_model_metrics():
#     if trainer.best_model is None:
#         trainer.load_model()
    
#     if trainer.metrics:
#         return {
#             "best_model": trainer.best_model_name,
#             "metrics": trainer.metrics
#         }
    
#     raise HTTPException(status_code=404, detail="No model metrics available")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..database import get_db
from ..models import City, AirQualityData, Prediction
from ..ml.model_trainer import ModelTrainer
from ..ml.feature_engineering import create_features
from ..utils.city_helper import add_city_to_database, fetch_and_store_aqi_for_city


router = APIRouter(prefix="/api", tags=["ml"])
trainer = ModelTrainer()


# -------------------------
# Response Schemas
# -------------------------

class TrainResponse(BaseModel):
    message: str
    metrics: dict


class PredictionResponse(BaseModel):
    city_name: str
    current_aqi: float
    predicted_aqi: float
    prediction_time: datetime
    model_version: str


# -------------------------
# Train Model Endpoint
# -------------------------

@router.post("/train-model", response_model=TrainResponse)
def train_model(city_name: str, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    aqi_data = (
        db.query(AirQualityData)
        .filter(AirQualityData.city_id == city.id)
        .order_by(AirQualityData.timestamp)
        .all()
    )

    if len(aqi_data) < 50:
        raise HTTPException(
            status_code=400,
            detail="Insufficient data for training (minimum 50 records)"
        )

    df = pd.DataFrame([
        {
            "timestamp": record.timestamp,
            "pm2_5": record.pm2_5,
            "pm10": record.pm10,
            "no2": record.no2,
            "so2": record.so2,
            "co": record.co,
            "o3": record.o3,
            "aqi": record.aqi
        }
        for record in aqi_data
    ])

    metrics = trainer.train_models(df)
    trainer.save_model()

    return {
        "message": f"Model trained successfully. Best model: {trainer.best_model_name}",
        "metrics": metrics
    }


# -------------------------
# Prediction Endpoint
# -------------------------

@router.get("/predict/{city_name}", response_model=PredictionResponse)
def predict_aqi(city_name: str, db: Session = Depends(get_db)):
    """
    Predict AQI for a city. If city doesn't exist in database:
    1. Fetch city coordinates from OpenWeather Geocoding API
    2. Add city to database
    3. Fetch current AQI data
    4. Store AQI data
    5. Perform prediction
    """

    # Check if city exists in database
    city = db.query(City).filter(City.name == city_name).first()
    
    # If city not found, dynamically add it
    if not city:
        print(f"City '{city_name}' not found in database. Attempting to add...")
        
        # Fetch coordinates and add city to database
        city = add_city_to_database(db, city_name)
        
        if not city:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city_name}' not found. Please check the city name and try again."
            )
        
        # Fetch and store current AQI data for the new city
        success = fetch_and_store_aqi_for_city(db, city)
        
        if not success:
            raise HTTPException(
                status_code=503,
                detail=f"City '{city_name}' added but unable to fetch AQI data. Please check API keys."
            )
        
        print(f"Successfully added city '{city_name}' and fetched initial AQI data")

    # Load model if not in memory
    if trainer.best_model is None:
        trainer.load_model()

    if trainer.best_model is None:
        raise HTTPException(status_code=400, detail="No trained model available")

    # Get recent data for prediction
    recent_data = (
        db.query(AirQualityData)
        .filter(AirQualityData.city_id == city.id)
        .order_by(desc(AirQualityData.timestamp))
        .limit(24)
        .all()
    )

    if len(recent_data) < 3:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient data for prediction. Found {len(recent_data)} records, need at least 3."
        )

    # Reverse to chronological order
    df = pd.DataFrame([
        {
            "timestamp": record.timestamp,
            "pm2_5": record.pm2_5,
            "pm10": record.pm10,
            "no2": record.no2,
            "so2": record.so2,
            "co": record.co,
            "o3": record.o3,
            "aqi": record.aqi
        }
        for record in reversed(recent_data)
    ])

    # Create features for prediction
    df_features = create_features(df)

    if df_features.empty:
        raise HTTPException(
            status_code=400,
            detail="Unable to create features for prediction"
        )

    # Define feature columns
    feature_columns = [
        "pm2_5",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3",
        "aqi_lag_1",
        "aqi_lag_2",
        "aqi_lag_3",
        "aqi_rolling_24h",
        "aqi_delta",
        "hour",
        "day_of_week",
        "month",
        "pm_ratio"
    ]

    # Get latest features
    latest_features = df_features.iloc[-1:][feature_columns]

    # Make prediction
    predicted_aqi = trainer.predict(latest_features)[0]

    prediction_time = datetime.utcnow() + timedelta(hours=1)

    # Store prediction in database
    prediction = Prediction(
        city_id=city.id,
        predicted_aqi=float(predicted_aqi),
        prediction_time=prediction_time,
        model_version=trainer.best_model_name
    )

    db.add(prediction)
    db.commit()

    return {
        "city_name": city.name,
        "current_aqi": float(recent_data[0].aqi),
        "predicted_aqi": float(predicted_aqi),
        "prediction_time": prediction_time,
        "model_version": trainer.best_model_name
    }


# -------------------------
# Model Metrics Endpoint
# -------------------------

@router.get("/model-metrics")
def get_model_metrics():

    if trainer.best_model is None:
        trainer.load_model()

    if trainer.metrics:
        return {
            "best_model": trainer.best_model_name,
            "metrics": trainer.metrics
        }

    raise HTTPException(status_code=404, detail="No model metrics available")


# -------------------------
# Predict Next 24 Hours
# -------------------------

@router.get("/predict-24h/{city_name}")
def predict_24h(city_name: str, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    if trainer.best_model is None:
        trainer.load_model()

    if trainer.best_model is None:
        raise HTTPException(status_code=400, detail="No trained model available")

    recent_data = (
        db.query(AirQualityData)
        .filter(AirQualityData.city_id == city.id)
        .order_by(desc(AirQualityData.timestamp))
        .limit(24)
        .all()
    )

    if len(recent_data) < 3:
        raise HTTPException(
            status_code=400,
            detail="Insufficient recent data for prediction"
        )

    predictions = []
    df = pd.DataFrame([
        {
            "timestamp": record.timestamp,
            "pm2_5": record.pm2_5,
            "pm10": record.pm10,
            "no2": record.no2,
            "so2": record.so2,
            "co": record.co,
            "o3": record.o3,
            "aqi": record.aqi
        }
        for record in reversed(recent_data)
    ])

    feature_columns = [
        "pm2_5", "pm10", "no2", "so2", "co", "o3",
        "aqi_lag_1", "aqi_lag_2", "aqi_lag_3",
        "aqi_rolling_24h", "aqi_delta",
        "hour", "day_of_week", "month", "pm_ratio"
    ]

    last_timestamp = df['timestamp'].iloc[-1]
    
    for i in range(24):
        df_features = create_features(df)
        
        if df_features.empty:
            break
            
        latest_features = df_features.iloc[-1:][feature_columns]
        predicted_aqi = trainer.predict(latest_features)[0]
        
        prediction_time = last_timestamp + timedelta(hours=i+1)
        
        predictions.append({
            "timestamp": prediction_time.isoformat(),
            "aqi": float(predicted_aqi),
            "pm2_5": float(df['pm2_5'].iloc[-1]),
            "pm10": float(df['pm10'].iloc[-1])
        })
        
        new_row = pd.DataFrame([{
            "timestamp": prediction_time,
            "pm2_5": df['pm2_5'].iloc[-1],
            "pm10": df['pm10'].iloc[-1],
            "no2": df['no2'].iloc[-1],
            "so2": df['so2'].iloc[-1],
            "co": df['co'].iloc[-1],
            "o3": df['o3'].iloc[-1],
            "aqi": predicted_aqi
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)

    return predictions