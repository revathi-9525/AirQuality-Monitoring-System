from app.database import SessionLocal, engine
from app.models import Base
from app.utils.seed_data import seed_cities, seed_sample_aqi_data

# Create tables
Base.metadata.create_all(bind=engine)

# Create database session
db = SessionLocal()

try:
    print("Seeding Indian cities...")
    seed_cities(db)
    print("[OK] Cities added successfully!")
    
    # List of Indian cities to populate with data
    indian_cities = [
        "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai",
        "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
        "Kanpur", "Nagpur", "Indore", "Patna", "Bhopal",
        "Chandigarh", "Gurgaon", "Noida", "Ghaziabad", "Faridabad"
    ]
    
    # Andhra Pradesh cities
    andhra_pradesh_cities = [
        "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool",
        "Rajahmundry", "Tirupati", "Kakinada", "Anantapur", "Kadapa",
        "Eluru", "Ongole", "Nandyal", "Machilipatnam", "Adoni"
    ]
    
    all_cities = indian_cities + andhra_pradesh_cities
    
    print("\nGenerating AQI data for all cities (30 days)...")
    for city in all_cities:
        print(f"  Generating data for {city}...")
        seed_sample_aqi_data(db, city, days=30)
    
    print("\n[OK] All cities populated with AQI data!")
    print(f"[OK] Total cities: {len(all_cities)}")
    print(f"  - Major Indian cities: {len(indian_cities)}")
    print(f"  - Andhra Pradesh cities: {len(andhra_pradesh_cities)}")
    print("[OK] Data range: Last 30 days (hourly)")
    
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()
