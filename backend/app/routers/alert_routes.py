from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import City, AirQualityData, Alert
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["alerts"])

class AlertResponse(BaseModel):
    id: int
    city_id: int
    aqi_value: float
    threshold: float
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AlertConfig(BaseModel):
    city_name: str
    threshold: float

@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(limit: int = 10, db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(desc(Alert.created_at)).limit(limit).all()
    return alerts

@router.post("/alerts/configure")
def configure_alert(config: AlertConfig, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.name == config.city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    latest_aqi = db.query(AirQualityData).filter(
        AirQualityData.city_id == city.id
    ).order_by(desc(AirQualityData.timestamp)).first()
    
    if latest_aqi and latest_aqi.aqi > config.threshold:
        alert = Alert(
            city_id=city.id,
            aqi_value=latest_aqi.aqi,
            threshold=config.threshold,
            message=f"AQI alert for {config.city_name}: Current AQI {latest_aqi.aqi:.1f} exceeds threshold {config.threshold}"
        )
        db.add(alert)
        db.commit()
        return {"message": "Alert created", "alert_triggered": True}
    
    return {"message": "Alert configured", "alert_triggered": False}

@router.get("/alerts/{city_name}", response_model=List[AlertResponse])
def get_city_alerts(city_name: str, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    alerts = db.query(Alert).filter(
        Alert.city_id == city.id
    ).order_by(desc(Alert.created_at)).limit(10).all()
    
    return alerts
