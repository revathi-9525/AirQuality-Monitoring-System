from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String)
    
    air_quality_data = relationship("AirQualityData", back_populates="city")
    predictions = relationship("Prediction", back_populates="city")

class AirQualityData(Base):
    __tablename__ = "air_quality_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    co = Column(Float)
    o3 = Column(Float)
    aqi = Column(Float)
    
    city = relationship("City", back_populates="air_quality_data")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    predicted_aqi = Column(Float)
    prediction_time = Column(DateTime)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    city = relationship("City", back_populates="predictions")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    aqi_value = Column(Float)
    threshold = Column(Float)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
