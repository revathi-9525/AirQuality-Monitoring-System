# AirVision AI - Air Quality Monitoring & Prediction System

## 🌟 Project Overview

AirVision AI is a full-stack AI-powered web application that monitors real-time air quality, stores historical pollution data, predicts future AQI using machine learning, and provides actionable insights through an intuitive dashboard.

## 🎯 Key Features

- **Real-Time AQI Monitoring**: Track air quality across multiple cities
- **Historical Data Analysis**: View trends and patterns over time
- **AI-Powered Predictions**: Forecast future AQI using ML models (Linear Regression, Random Forest, XGBoost)
- **Smart Alerts**: Get notified when air quality reaches unhealthy levels
- **Interactive Dashboard**: Visualize data with charts and graphs
- **Multi-City Support**: Monitor air quality in different locations
- **Model Performance Metrics**: Compare ML models with MAE, RMSE, and R² scores

## 🏗️ Architecture

```
aqi-project/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Database models
│   │   ├── database.py          # Database configuration
│   │   ├── routers/             # API endpoints
│   │   │   ├── data_routes.py
│   │   │   ├── ml_routes.py
│   │   │   └── alert_routes.py
│   │   ├── services/            # Business logic
│   │   │   └── data_fetcher.py
│   │   ├── ml/                  # Machine learning
│   │   │   ├── model_trainer.py
│   │   │   └── feature_engineering.py
│   │   └── utils/               # Utilities
│   │       └── seed_data.py
│   ├── data/                    # Data storage
│   ├── trained_models/          # Saved ML models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── utils/               # Utility functions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Pandas & NumPy** - Data processing
- **Scikit-learn** - ML models
- **XGBoost** - Gradient boosting

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

5. Initialize database and seed sample data:
```bash
python setup.py
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
copy .env.example .env
```

4. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📊 API Endpoints

### Data Endpoints
- `GET /api/cities` - Get all cities
- `GET /api/aqi/{city_name}` - Get current AQI for a city
- `GET /api/aqi/history/{city_name}` - Get historical AQI data

### ML Endpoints
- `POST /api/train-model?city_name={city}` - Train ML model
- `GET /api/predict/{city_name}` - Predict future AQI
- `GET /api/model-metrics` - Get model performance metrics

### Alert Endpoints
- `GET /api/alerts` - Get recent alerts
- `POST /api/alerts/configure` - Configure alert threshold

## 🤖 Machine Learning

### Models Implemented
1. **Linear Regression** - Baseline model
2. **Random Forest** - Ensemble method
3. **XGBoost** - Gradient boosting

### Features Used
- Pollutant levels (PM2.5, PM10, NO2, SO2, CO, O3)
- Lag features (t-1, t-2, t-3)
- Rolling averages (24-hour)
- Temporal features (hour, day, month)
- Trend indicators

### Evaluation Metrics
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score** (Coefficient of Determination)

## 🎨 UI Features

### Dashboard
- City selector
- Current AQI display with color coding
- Historical trend charts
- Pollutant breakdown
- Real-time data updates

### Prediction Page
- Model training interface
- AQI prediction for next hour
- Model performance comparison
- Metrics visualization

### Analytics Page
- Multi-day trend analysis
- Comparative pollutant charts
- Alert history
- Customizable time periods

## 🔔 Alert System

The system monitors AQI levels and triggers alerts when thresholds are exceeded:
- **Green (0-50)**: Good
- **Yellow (51-100)**: Moderate
- **Orange (101-200)**: Unhealthy
- **Red (201-300)**: Very Unhealthy
- **Purple (300+)**: Hazardous

## 📈 Data Sources

- OpenWeatherMap API
- World Air Quality Index Project API

## 🧪 Testing

### Seed Sample Data
```python
from app.database import SessionLocal
from app.utils.seed_data import seed_cities, seed_sample_aqi_data

db = SessionLocal()
seed_cities(db)
seed_sample_aqi_data(db, "Delhi", days=30)
```

## 🚢 Deployment

### Backend (Render)
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Import GitHub repository
2. Framework preset: Vite
3. Build command: `npm run build`
4. Output directory: `dist`

## 📝 Future Enhancements

- [ ] LSTM time-series forecasting
- [ ] User authentication
- [ ] Email/SMS alerts
- [ ] Mobile app
- [ ] Data drift detection
- [ ] Model retraining pipeline
- [ ] Redis caching
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ for cleaner air and healthier communities.

## 📞 Support

For issues and questions, please open an issue on GitHub.
