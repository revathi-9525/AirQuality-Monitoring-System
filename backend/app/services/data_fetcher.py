import requests
import os
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import City, AirQualityData

class DataFetcher:
    def __init__(self):
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY")
        self.waqi_key = os.getenv("WAQI_API_KEY")
    
    def fetch_openweather_aqi(self, lat: float, lon: float):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.openweather_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            components = data['list'][0]['components']
            aqi = data['list'][0]['main']['aqi']
            
            return {
                'pm2_5': components.get('pm2_5', 0),
                'pm10': components.get('pm10', 0),
                'no2': components.get('no2', 0),
                'so2': components.get('so2', 0),
                'co': components.get('co', 0),
                'o3': components.get('o3', 0),
                'aqi': aqi * 50
            }
        except Exception as e:
            print(f"Error fetching OpenWeather data: {e}")
            return None
    
    def fetch_waqi_aqi(self, city_name: str):
        url = f"https://api.waqi.info/feed/{city_name}/?token={self.waqi_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok':
                return None
            
            iaqi = data['data'].get('iaqi', {})
            
            return {
                'pm2_5': iaqi.get('pm25', {}).get('v', 0),
                'pm10': iaqi.get('pm10', {}).get('v', 0),
                'no2': iaqi.get('no2', {}).get('v', 0),
                'so2': iaqi.get('so2', {}).get('v', 0),
                'co': iaqi.get('co', {}).get('v', 0),
                'o3': iaqi.get('o3', {}).get('v', 0),
                'aqi': data['data'].get('aqi', 0)
            }
        except Exception as e:
            print(f"Error fetching WAQI data: {e}")
            return None
    
    def store_aqi_data(self, db: Session, city_id: int, aqi_data: dict):
        db_aqi = AirQualityData(
            city_id=city_id,
            timestamp=datetime.utcnow(),
            **aqi_data
        )
        db.add(db_aqi)
        db.commit()
        db.refresh(db_aqi)
        return db_aqi
