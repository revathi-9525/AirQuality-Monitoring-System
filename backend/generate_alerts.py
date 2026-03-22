from app.database import SessionLocal
from app.models import City, AirQualityData, Alert
from sqlalchemy import desc
from datetime import datetime, timedelta

db = SessionLocal()

try:
    print("=" * 50)
    print("  Generating Sample Alerts")
    print("=" * 50)
    
    # Delete existing alerts
    deleted = db.query(Alert).delete()
    db.commit()
    print(f"\n[OK] Deleted {deleted} old alerts")
    
    # Get all cities
    cities = db.query(City).all()
    alerts_created = 0
    
    print("\nGenerating alerts for cities with high AQI...\n")
    
    for city in cities:
        # Get recent AQI data for this city
        recent_data = db.query(AirQualityData).filter(
            AirQualityData.city_id == city.id
        ).order_by(desc(AirQualityData.timestamp)).limit(24).all()
        
        if not recent_data:
            continue
        
        # Check for AQI values above thresholds
        for data in recent_data:
            alert_created = False
            
            # Hazardous (300+)
            if data.aqi >= 300:
                alert = Alert(
                    city_id=city.id,
                    aqi_value=data.aqi,
                    threshold=300,
                    message=f"HAZARDOUS: {city.name} AQI reached {data.aqi:.0f}! Stay indoors and avoid all outdoor activities.",
                    created_at=data.timestamp
                )
                db.add(alert)
                alert_created = True
            
            # Very Unhealthy (201-300)
            elif data.aqi >= 201:
                alert = Alert(
                    city_id=city.id,
                    aqi_value=data.aqi,
                    threshold=201,
                    message=f"VERY UNHEALTHY: {city.name} AQI is {data.aqi:.0f}. Health warnings for everyone.",
                    created_at=data.timestamp
                )
                db.add(alert)
                alert_created = True
            
            # Unhealthy (101-200)
            elif data.aqi >= 150:
                alert = Alert(
                    city_id=city.id,
                    aqi_value=data.aqi,
                    threshold=150,
                    message=f"UNHEALTHY: {city.name} AQI is {data.aqi:.0f}. Sensitive groups should limit outdoor exposure.",
                    created_at=data.timestamp
                )
                db.add(alert)
                alert_created = True
            
            if alert_created:
                alerts_created += 1
                print(f"  Alert created for {city.name:20s} - AQI: {data.aqi:.0f}")
                break  # Only create one alert per city
    
    db.commit()
    
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print(f"[OK] Total alerts created: {alerts_created}")
    
    # Show recent alerts
    recent_alerts = db.query(Alert).order_by(desc(Alert.created_at)).limit(10).all()
    
    if recent_alerts:
        print("\nRecent Alerts:")
        for alert in recent_alerts:
            city = db.query(City).filter(City.id == alert.city_id).first()
            print(f"  - {city.name}: AQI {alert.aqi_value:.0f} at {alert.created_at}")
    
    print("\n" + "=" * 50)
    print("  Complete!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    db.rollback()
finally:
    db.close()
