"""
Quick API Reference - Enhanced Prediction Endpoint
"""

# ============================================
# ENHANCED PREDICTION ENDPOINT
# ============================================

# Endpoint: GET /api/predict/{city_name}
# Description: Predict AQI for any city (auto-adds if not in database)

# ============================================
# EXAMPLE 1: Existing City
# ============================================

# Request:
GET http://localhost:8000/api/predict/Delhi

# Response (200 OK):
{
  "city_name": "Delhi",
  "current_aqi": 156.5,
  "predicted_aqi": 162.3,
  "prediction_time": "2024-01-15T10:00:00.000Z",
  "model_version": "XGBoost"
}

# ============================================
# EXAMPLE 2: New City (Auto-adds)
# ============================================

# Request:
GET http://localhost:8000/api/predict/Tokyo

# What happens internally:
# 1. Check database → Tokyo not found
# 2. Call OpenWeather Geocoding API → Get coordinates
# 3. Insert Tokyo into City table
# 4. Fetch current AQI data from OpenWeather/WAQI
# 5. Store AQI data in AirQualityData table
# 6. Create features and make prediction
# 7. Store prediction in Predictions table
# 8. Return prediction

# Response (200 OK):
{
  "city_name": "Tokyo",
  "current_aqi": 45.2,
  "predicted_aqi": 48.7,
  "prediction_time": "2024-01-15T10:00:00.000Z",
  "model_version": "XGBoost"
}

# ============================================
# EXAMPLE 3: Invalid City
# ============================================

# Request:
GET http://localhost:8000/api/predict/InvalidCity123

# Response (404 Not Found):
{
  "detail": "City 'InvalidCity123' not found. Please check the city name and try again."
}

# ============================================
# EXAMPLE 4: API Key Missing
# ============================================

# Request:
GET http://localhost:8000/api/predict/Sydney

# Response (503 Service Unavailable):
{
  "detail": "City 'Sydney' added but unable to fetch AQI data. Please check API keys."
}

# ============================================
# EXAMPLE 5: Insufficient Data
# ============================================

# Request:
GET http://localhost:8000/api/predict/Barcelona

# Response (400 Bad Request):
{
  "detail": "Insufficient data for prediction. Found 1 records, need at least 3."
}

# Solution: Generate sample data
POST http://localhost:8000/api/aqi/generate-sample/Barcelona?hours=24

# Then retry prediction
GET http://localhost:8000/api/predict/Barcelona

# ============================================
# VERIFY CITY ADDED TO DATABASE
# ============================================

# Request:
GET http://localhost:8000/api/cities

# Response (200 OK):
[
  {
    "id": 1,
    "name": "Delhi",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "country": "IN"
  },
  {
    "id": 2,
    "name": "Mumbai",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "country": "IN"
  },
  {
    "id": 6,
    "name": "Tokyo",
    "latitude": 35.6762,
    "longitude": 139.6503,
    "country": "JP"
  }
]

# ============================================
# FRONTEND USAGE (No Changes Needed!)
# ============================================

# JavaScript/React Example:
const predictAQI = async (cityName) => {
  try {
    const response = await fetch(`/api/predict/${cityName}`);
    const data = await response.json();
    
    if (response.ok) {
      console.log(`Current AQI: ${data.current_aqi}`);
      console.log(`Predicted AQI: ${data.predicted_aqi}`);
      // City automatically added if new!
    } else {
      console.error(data.detail);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

// Works for existing cities
await predictAQI('Delhi');

// Works for new cities (auto-adds)
await predictAQI('Paris');
await predictAQI('Singapore');
await predictAQI('Dubai');

# ============================================
# CURL EXAMPLES
# ============================================

# Predict for existing city
curl http://localhost:8000/api/predict/Delhi

# Predict for new city (auto-adds)
curl http://localhost:8000/api/predict/Paris

# Get all cities (including newly added)
curl http://localhost:8000/api/cities

# Generate sample data for new city
curl -X POST "http://localhost:8000/api/aqi/generate-sample/Paris?hours=24"

# ============================================
# PYTHON REQUESTS EXAMPLES
# ============================================

import requests

# Predict for any city
response = requests.get('http://localhost:8000/api/predict/London')
if response.status_code == 200:
    data = response.json()
    print(f"City: {data['city_name']}")
    print(f"Current AQI: {data['current_aqi']}")
    print(f"Predicted AQI: {data['predicted_aqi']}")
else:
    print(f"Error: {response.json()['detail']}")

# ============================================
# ERROR CODES
# ============================================

# 200 OK - Prediction successful
# 400 Bad Request - Insufficient data or no model
# 404 Not Found - City not found in geocoding API
# 503 Service Unavailable - AQI data fetch failed

# ============================================
# ENVIRONMENT VARIABLES REQUIRED
# ============================================

# .env file:
OPENWEATHER_API_KEY=your_api_key_here
WAQI_API_KEY=your_waqi_key_here  # Optional

# ============================================
# TESTING CITIES
# ============================================

# Major cities that should work:
# - New York, London, Paris, Tokyo, Sydney
# - Singapore, Dubai, Toronto, Berlin, Rome
# - Madrid, Amsterdam, Stockholm, Oslo, Vienna

# Cities that might fail (small/ambiguous):
# - Springfield (too many)
# - XYZ123 (invalid)
# - Atlantis (doesn't exist)
