import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame):
    df = df.sort_values('timestamp').copy()
    
    # Lag features
    df['aqi_lag_1'] = df['aqi'].shift(1)
    df['aqi_lag_2'] = df['aqi'].shift(2)
    df['aqi_lag_3'] = df['aqi'].shift(3)
    
    # Rolling mean (24-hour average)
    df['aqi_rolling_24h'] = df['aqi'].rolling(window=24, min_periods=1).mean()
    
    # Trend delta
    df['aqi_delta'] = df['aqi'] - df['aqi'].shift(1)
    
    # Seasonal encoding
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    
    # Pollutant ratios
    df['pm_ratio'] = df['pm2_5'] / (df['pm10'] + 1)
    
    df = df.dropna()
    return df

def prepare_training_data(df: pd.DataFrame):
    feature_cols = [
        'pm2_5', 'pm10', 'no2', 'so2', 'co', 'o3',
        'aqi_lag_1', 'aqi_lag_2', 'aqi_lag_3',
        'aqi_rolling_24h', 'aqi_delta',
        'hour', 'day_of_week', 'month', 'pm_ratio'
    ]
    
    X = df[feature_cols]
    y = df['aqi']
    
    return X, y
