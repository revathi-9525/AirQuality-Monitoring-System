from sqlalchemy.orm import Session
from ..models import City, AirQualityData
from datetime import datetime, timedelta
import random

def seed_cities(db: Session):
    cities_data = [
        # Major Indian Cities
        {"name": "Delhi", "latitude": 28.6139, "longitude": 77.2090, "country": "India"},
        {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "country": "India"},
        {"name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946, "country": "India"},
        {"name": "Kolkata", "latitude": 22.5726, "longitude": 88.3639, "country": "India"},
        {"name": "Chennai", "latitude": 13.0827, "longitude": 80.2707, "country": "India"},
        {"name": "Hyderabad", "latitude": 17.3850, "longitude": 78.4867, "country": "India"},
        {"name": "Pune", "latitude": 18.5204, "longitude": 73.8567, "country": "India"},
        {"name": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "country": "India"},
        {"name": "Jaipur", "latitude": 26.9124, "longitude": 75.7873, "country": "India"},
        {"name": "Lucknow", "latitude": 26.8467, "longitude": 80.9462, "country": "India"},
        {"name": "Kanpur", "latitude": 26.4499, "longitude": 80.3319, "country": "India"},
        {"name": "Nagpur", "latitude": 21.1458, "longitude": 79.0882, "country": "India"},
        {"name": "Indore", "latitude": 22.7196, "longitude": 75.8577, "country": "India"},
        {"name": "Patna", "latitude": 25.5941, "longitude": 85.1376, "country": "India"},
        {"name": "Bhopal", "latitude": 23.2599, "longitude": 77.4126, "country": "India"},
        {"name": "Chandigarh", "latitude": 30.7333, "longitude": 76.7794, "country": "India"},
        {"name": "Gurgaon", "latitude": 28.4595, "longitude": 77.0266, "country": "India"},
        {"name": "Noida", "latitude": 28.5355, "longitude": 77.3910, "country": "India"},
        {"name": "Ghaziabad", "latitude": 28.6692, "longitude": 77.4538, "country": "India"},
        {"name": "Faridabad", "latitude": 28.4089, "longitude": 77.3178, "country": "India"},
        
        # Andhra Pradesh Cities
        {"name": "Visakhapatnam", "latitude": 17.6869, "longitude": 83.2185, "country": "India"},
        {"name": "Vijayawada", "latitude": 16.5062, "longitude": 80.6480, "country": "India"},
        {"name": "Guntur", "latitude": 16.3067, "longitude": 80.4365, "country": "India"},
        {"name": "Nellore", "latitude": 14.4426, "longitude": 79.9865, "country": "India"},
        {"name": "Kurnool", "latitude": 15.8281, "longitude": 78.0373, "country": "India"},
        {"name": "Rajahmundry", "latitude": 17.0005, "longitude": 81.8040, "country": "India"},
        {"name": "Tirupati", "latitude": 13.6288, "longitude": 79.4192, "country": "India"},
        {"name": "Kakinada", "latitude": 16.9891, "longitude": 82.2475, "country": "India"},
        {"name": "Anantapur", "latitude": 14.6819, "longitude": 77.6006, "country": "India"},
        {"name": "Kadapa", "latitude": 14.4673, "longitude": 78.8242, "country": "India"},
        {"name": "Eluru", "latitude": 16.7107, "longitude": 81.0950, "country": "India"},
        {"name": "Ongole", "latitude": 15.5057, "longitude": 80.0499, "country": "India"},
        {"name": "Nandyal", "latitude": 15.4769, "longitude": 78.4830, "country": "India"},
        {"name": "Machilipatnam", "latitude": 16.1875, "longitude": 81.1389, "country": "India"},
        {"name": "Adoni", "latitude": 15.6281, "longitude": 77.2750, "country": "India"},
    ]
    
    for city_data in cities_data:
        existing = db.query(City).filter(City.name == city_data["name"]).first()
        if not existing:
            city = City(**city_data)
            db.add(city)
    
    db.commit()

def seed_sample_aqi_data(db: Session, city_name: str, days: int = 30):
    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        return
    
    base_time = datetime.utcnow() - timedelta(days=days)
    
    for i in range(days * 24):
        timestamp = base_time + timedelta(hours=i)
        
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
