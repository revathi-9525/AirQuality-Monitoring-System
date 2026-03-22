from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import City, AirQualityData
from ..services.data_fetcher import DataFetcher
from ..utils.city_helper import add_city_to_database, fetch_and_store_aqi_for_city
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["data"])

data_fetcher = DataFetcher()

class CityResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    country: str
    
    class Config:
        from_attributes = True

class AQIResponse(BaseModel):
    id: int
    timestamp: datetime
    pm2_5: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    aqi: float
    
    class Config:
        from_attributes = True

@router.get("/cities", response_model=List[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities

@router.get("/aqi/{city_name}", response_model=AQIResponse)
def get_current_aqi(city_name: str, db: Session = Depends(get_db)):
    """
    Get current AQI for a city. If city doesn't exist:
    1. Fetch city coordinates from OpenWeather Geocoding API
    2. Add city to database
    3. Fetch current AQI data
    4. Store AQI data
    5. Return AQI data
    """
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
    
    latest_aqi = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id
    ).order_by(desc(AirQualityData.timestamp)).first()
    
    if not latest_aqi:
        raise HTTPException(status_code=404, detail="No AQI data available")
    
    return latest_aqi

@router.get("/aqi/history/{city_name}", response_model=List[AQIResponse])
def get_aqi_history(city_name: str, days: int = 7, db: Session = Depends(get_db)):
    """
    Get AQI history for a city. If city doesn't exist:
    1. Fetch city coordinates from OpenWeather Geocoding API
    2. Add city to database
    3. Fetch current AQI data
    4. Store AQI data
    5. Return history
    """
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
    
    start_date = datetime.utcnow() - timedelta(days=days)
    history = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id,
        AirQualityData.timestamp >= start_date
    ).order_by(AirQualityData.timestamp).all()
    
    return history


@router.post("/aqi/refresh/{city_name}")
def refresh_aqi_data(city_name: str, db: Session = Depends(get_db)):
    """Fetch and store current AQI data for a city"""
    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Try to fetch from OpenWeather first, then WAQI
    aqi_data = None
    
    if city.latitude and city.longitude:
        aqi_data = data_fetcher.fetch_openweather_aqi(city.latitude, city.longitude)
    
    if not aqi_data:
        aqi_data = data_fetcher.fetch_waqi_aqi(city_name)
    
    if not aqi_data:
        raise HTTPException(
            status_code=503, 
            detail="Unable to fetch AQI data. Check API keys configuration."
        )
    
    # Store the data
    stored_data = data_fetcher.store_aqi_data(db, city.id, aqi_data)
    
    return {
        "message": f"AQI data refreshed for {city_name}",
        "data": {
            "timestamp": stored_data.timestamp.isoformat(),
            "aqi": stored_data.aqi,
            "pm2_5": stored_data.pm2_5,
            "pm10": stored_data.pm10
        }
    }


@router.post("/aqi/refresh-all")
def refresh_all_cities(db: Session = Depends(get_db)):
    """Fetch and store current AQI data for all cities"""
    cities = db.query(City).all()
    results = []
    
    for city in cities:
        aqi_data = None
        
        if city.latitude and city.longitude:
            aqi_data = data_fetcher.fetch_openweather_aqi(city.latitude, city.longitude)
        
        if not aqi_data:
            aqi_data = data_fetcher.fetch_waqi_aqi(city.name)
        
        if aqi_data:
            data_fetcher.store_aqi_data(db, city.id, aqi_data)
            results.append({"city": city.name, "status": "success"})
        else:
            results.append({"city": city.name, "status": "failed"})
    
    return {
        "message": "AQI data refresh completed",
        "results": results
    }


@router.post("/aqi/generate-sample/{city_name}")
def generate_sample_data(city_name: str, hours: int = 24, db: Session = Depends(get_db)):
    """Generate sample AQI data for testing (without external API)"""
    import random
    from datetime import datetime, timedelta
    
    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Delete existing data for this city
    db.query(AirQualityData).filter(AirQualityData.city_id == city.id).delete()
    
    now = datetime.utcnow()
    
    for i in range(hours):
        # Start from hours ago and increment forward
        timestamp = now - timedelta(hours=hours-1-i)
        
        aqi_base = random.uniform(50, 200)
        aqi_data = AirQualityData(
            city_id=city.id,
            timestamp=timestamp,
            pm2_5=random.uniform(10, 150),
            pm10=random.uniform(20, 200),
            no2=random.uniform(10, 100),
            so2=random.uniform(5, 50),
            co=random.uniform(0.1, 5),
            o3=random.uniform(10, 100),
            aqi=aqi_base + random.uniform(-10, 10)
        )
        db.add(aqi_data)
    
    db.commit()
    
    return {
        "message": f"Generated {hours} hours of sample data for {city_name}",
        "city": city_name,
        "hours": hours
    }


@router.post("/aqi/generate-sample-all")
def generate_sample_data_all(hours: int = 720, db: Session = Depends(get_db)):
    """Generate sample AQI data for all cities (without external API)"""
    import random
    from datetime import datetime, timedelta
    
    cities = db.query(City).all()
    records_created = 0
    
    for city in cities:
        # Delete ALL existing data for this city first
        db.query(AirQualityData).filter(AirQualityData.city_id == city.id).delete()
        
        # Generate data from (hours) ago up to now
        now = datetime.utcnow()
        
        for i in range(hours):
            # Start from hours ago and increment forward
            timestamp = now - timedelta(hours=hours-1-i)
            
            aqi_base = random.uniform(50, 200)
            aqi_data = AirQualityData(
                city_id=city.id,
                timestamp=timestamp,
                pm2_5=random.uniform(10, 150),
                pm10=random.uniform(20, 200),
                no2=random.uniform(10, 100),
                so2=random.uniform(5, 50),
                co=random.uniform(0.1, 5),
                o3=random.uniform(10, 100),
                aqi=aqi_base + random.uniform(-10, 10)
            )
            db.add(aqi_data)
            records_created += 1
    
    db.commit()
    
    return {
        "message": f"Generated {hours} hours of sample data for all cities",
        "cities_count": len(cities),
        "hours": hours,
        "total_records": records_created
    }
