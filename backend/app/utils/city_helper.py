"""
Helper functions for dynamic city addition and data fetching
"""
import os
import requests
from sqlalchemy.orm import Session
from ..models import City
from ..services.data_fetcher import DataFetcher


def fetch_city_coordinates(city_name: str) -> dict:
    """
    Fetch city coordinates using OpenWeather Geocoding API
    
    Args:
        city_name: Name of the city to search
        
    Returns:
        dict with keys: name, lat, lon, country
        None if city not found or API error
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("OPENWEATHER_API_KEY not found in environment")
        return None
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data or len(data) == 0:
            print(f"City '{city_name}' not found in geocoding API")
            return None
        
        city_data = data[0]
        
        return {
            "name": city_data.get("name"),
            "lat": city_data.get("lat"),
            "lon": city_data.get("lon"),
            "country": city_data.get("country", "Unknown")
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching city coordinates: {e}")
        return None


def add_city_to_database(db: Session, city_name: str) -> City:
    """
    Fetch city coordinates and add to database
    
    Args:
        db: Database session
        city_name: Name of the city to add
        
    Returns:
        City object if successful
        None if failed
    """
    # Fetch coordinates from geocoding API
    city_info = fetch_city_coordinates(city_name)
    
    if not city_info:
        return None
    
    # Create new city record
    new_city = City(
        name=city_info["name"],
        latitude=city_info["lat"],
        longitude=city_info["lon"],
        country=city_info["country"]
    )
    
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    
    print(f"Added new city: {new_city.name}, {new_city.country}")
    
    return new_city


def fetch_and_store_aqi_for_city(db: Session, city: City, generate_history: bool = True) -> bool:
    """
    Fetch current AQI data for a city and store in database
    
    Args:
        db: Database session
        city: City object
        generate_history: If True, generate 30 days of historical data
        
    Returns:
        True if successful, False otherwise
    """
    data_fetcher = DataFetcher()
    
    # Try OpenWeather API first (requires coordinates)
    aqi_data = None
    if city.latitude and city.longitude:
        aqi_data = data_fetcher.fetch_openweather_aqi(city.latitude, city.longitude)
    
    # Fallback to WAQI API
    if not aqi_data:
        aqi_data = data_fetcher.fetch_waqi_aqi(city.name)
    
    if not aqi_data:
        print(f"Failed to fetch AQI data for {city.name}")
        return False
    
    # Store the current data
    data_fetcher.store_aqi_data(db, city.id, aqi_data)
    print(f"Stored AQI data for {city.name}: AQI={aqi_data['aqi']}")
    
    # Generate historical data for predictions (last 30 days = 720 hours)
    if generate_history:
        from datetime import datetime, timedelta
        import random
        from ..models import AirQualityData
        
        print(f"Generating 30 days of historical data for {city.name}...")
        
        now = datetime.utcnow()
        base_aqi = aqi_data['aqi']
        
        # Generate 719 more records (we already have 1 current record)
        # Total will be 720 records (30 days * 24 hours)
        for i in range(1, 720):
            timestamp = now - timedelta(hours=720-i)
            
            # Create realistic variations around the current AQI
            variation = random.uniform(-30, 30)
            historical_aqi = max(10, min(300, base_aqi + variation))
            
            historical_data = AirQualityData(
                city_id=city.id,
                timestamp=timestamp,
                pm2_5=max(1, aqi_data['pm2_5'] + random.uniform(-20, 20)),
                pm10=max(1, aqi_data['pm10'] + random.uniform(-30, 30)),
                no2=max(0.1, aqi_data['no2'] + random.uniform(-10, 10)),
                so2=max(0.1, aqi_data['so2'] + random.uniform(-5, 5)),
                co=max(0.1, aqi_data['co'] + random.uniform(-100, 100)),
                o3=max(1, aqi_data['o3'] + random.uniform(-20, 20)),
                aqi=historical_aqi
            )
            db.add(historical_data)
        
        db.commit()
        print(f"Generated 720 hours (30 days) of historical data for {city.name}")
    
    return True
