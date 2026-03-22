"""
Run this once after cloning to initialize the database and seed sample data.
Usage: python setup.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app import models
from app.utils.seed_data import seed_cities, seed_sample_aqi_data

def main():
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding cities...")
        seed_cities(db)

        print("Seeding sample AQI data for key cities...")
        for city in ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"]:
            seed_sample_aqi_data(db, city, days=30)
            print(f"  ✓ {city}")

        print("\nSetup complete! You can now run: uvicorn app.main:app --reload")
    finally:
        db.close()

if __name__ == "__main__":
    main()
