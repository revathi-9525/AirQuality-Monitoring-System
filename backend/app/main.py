from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncio
import random
from datetime import datetime, timedelta

from .database import engine, Base, SessionLocal
from .models import City, AirQualityData
from .routers import data_routes, ml_routes, alert_routes


# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)


def backfill_missing_records():
    """On startup, fill in any missing hourly records since last recorded timestamp."""
    db = SessionLocal()
    try:
        cities = db.query(City).all()
        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

        for city in cities:
            latest = db.query(AirQualityData).filter(
                AirQualityData.city_id == city.id
            ).order_by(AirQualityData.timestamp.desc()).first()

            if not latest:
                continue

            # Round latest timestamp down to the hour
            last_ts = latest.timestamp.replace(minute=0, second=0, microsecond=0)

            # Calculate how many hours are missing
            missing_hours = int((now - last_ts).total_seconds() // 3600)

            if missing_hours <= 0:
                continue

            base_aqi = latest.aqi
            base = latest

            for h in range(1, missing_hours + 1):
                timestamp = last_ts + timedelta(hours=h)
                new_aqi = max(10, min(300, base_aqi + random.uniform(-15, 15)))

                record = AirQualityData(
                    city_id=city.id,
                    timestamp=timestamp,
                    pm2_5=max(1, base.pm2_5 + random.uniform(-10, 10)),
                    pm10=max(1, base.pm10 + random.uniform(-15, 15)),
                    no2=max(0.1, base.no2 + random.uniform(-5, 5)),
                    so2=max(0.1, base.so2 + random.uniform(-3, 3)),
                    co=max(0.1, base.co + random.uniform(-0.2, 0.2)),
                    o3=max(1, base.o3 + random.uniform(-10, 10)),
                    aqi=new_aqi
                )
                db.add(record)
                base_aqi = new_aqi

            print(f"[Backfill] {city.name}: filled {missing_hours} missing hour(s)")

        db.commit()
        print("[Backfill] Complete.")
    except Exception as e:
        print(f"[Backfill] Error: {e}")
        db.rollback()
    finally:
        db.close()


async def auto_append_aqi():
    """Background task: appends one new AQI record per city every hour."""
    while True:
        await asyncio.sleep(3600)  # wait 1 hour
        db = SessionLocal()
        try:
            cities = db.query(City).all()
            now = datetime.utcnow()
            for city in cities:
                latest = db.query(AirQualityData).filter(
                    AirQualityData.city_id == city.id
                ).order_by(AirQualityData.timestamp.desc()).first()

                base_aqi = latest.aqi if latest else random.uniform(50, 200)
                new_aqi = max(10, min(300, base_aqi + random.uniform(-15, 15)))

                record = AirQualityData(
                    city_id=city.id,
                    timestamp=now,
                    pm2_5=max(1, (latest.pm2_5 if latest else 50) + random.uniform(-10, 10)),
                    pm10=max(1, (latest.pm10 if latest else 80) + random.uniform(-15, 15)),
                    no2=max(0.1, (latest.no2 if latest else 30) + random.uniform(-5, 5)),
                    so2=max(0.1, (latest.so2 if latest else 15) + random.uniform(-3, 3)),
                    co=max(0.1, (latest.co if latest else 1) + random.uniform(-0.2, 0.2)),
                    o3=max(1, (latest.o3 if latest else 40) + random.uniform(-10, 10)),
                    aqi=new_aqi
                )
                db.add(record)
            db.commit()
            print(f"[Scheduler] Appended hourly AQI records for {len(cities)} cities at {now}")
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
            db.rollback()
        finally:
            db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    backfill_missing_records()  # Fill gaps from when server was offline
    asyncio.create_task(auto_append_aqi())  # Keep adding every hour
    yield


# Initialize FastAPI app
app = FastAPI(
    title="AirVision AI API",
    description="AI-powered Air Quality Monitoring & Prediction System",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data_routes.router)
app.include_router(ml_routes.router)
app.include_router(alert_routes.router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AirVision AI - Air Quality Monitoring System",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Debug endpoint to check environment variables
@app.get("/debug/env")
def check_env():
    import os
    api_key = os.getenv("OPENWEATHER_API_KEY")
    return {
        "api_key_set": api_key is not None,
        "api_key_length": len(api_key) if api_key else 0,
        "api_key_preview": api_key[:10] + "..." if api_key else "NOT SET"
    }