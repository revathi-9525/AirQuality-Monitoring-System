import sys
sys.path.append('.')

from app.database import SessionLocal, engine, Base
from app.models import City, AirQualityData, Prediction, Alert
from app.utils.seed_data import seed_cities, seed_sample_aqi_data

def setup_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")
    
    db = SessionLocal()
    
    print("\nSeeding cities...")
    seed_cities(db)
    print("✓ Cities seeded")
    
    print("\nSeeding sample AQI data...")
    cities = ["Delhi", "Mumbai", "Beijing", "London", "NewYork"]
    for city in cities:
        print(f"  Seeding data for {city}...")
        seed_sample_aqi_data(db, city, days=30)
    print("✓ Sample data seeded")
    
    db.close()
    print("\n✅ Database setup complete!")
    print("\nYou can now start the server with:")
    print("  uvicorn app.main:app --reload")

if __name__ == "__main__":
    setup_database()
