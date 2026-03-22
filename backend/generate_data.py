from app.database import SessionLocal
from app.models import AirQualityData, City
from datetime import datetime, timedelta
import random

db = SessionLocal()

cities = db.query(City).all()
print(f'Generating data for {len(cities)} cities...\n')

hours = 720  # 30 days

for city in cities:
    # Delete ALL existing data
    deleted = db.query(AirQualityData).filter(AirQualityData.city_id == city.id).delete()
    print(f'{city.name}: Deleted {deleted} old records')
    
    # Generate new data
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
    
    # Verify counts
    total = db.query(AirQualityData).filter(AirQualityData.city_id == city.id).count()
    
    start_24h = datetime.utcnow() - timedelta(days=1)
    count_24h = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id,
        AirQualityData.timestamp >= start_24h
    ).count()
    
    start_7d = datetime.utcnow() - timedelta(days=7)
    count_7d = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id,
        AirQualityData.timestamp >= start_7d
    ).count()
    
    start_30d = datetime.utcnow() - timedelta(days=30)
    count_30d = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id,
        AirQualityData.timestamp >= start_30d
    ).count()
    
    print(f'{city.name}: Created {total} records')
    print(f'  Last 24h: {count_24h} records (Expected: 24)')
    print(f'  Last 7d: {count_7d} records (Expected: 168)')
    print(f'  Last 30d: {count_30d} records (Expected: 720)')
    print()

db.close()
print('Done!')
