import React, { useState, useEffect } from 'react';
import { getCities, trainModel, predictAQI, getModelMetrics } from '../services/api';
import { getAQICategory } from '../utils/aqiUtils';
import CitySearch from '../components/CitySearch';
import AQIHealthAdvice from '../components/AQIHealthAdvice';

const Prediction = () => {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [training, setTraining] = useState(false);

  useEffect(() => {
    loadCities();
    loadMetrics();
  }, []);

  const loadCities = async () => {
    try {
      const response = await getCities();
      setCities(response.data);
      if (response.data.length > 0) {
        setSelectedCity(response.data[0].name);
      }
    } catch (error) {
      console.error('Error loading cities:', error);
    }
  };

  const loadMetrics = async () => {
    try {
      const response = await getModelMetrics();
      setMetrics(response.data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    }
  };

  const handleTrain = async () => {
    setTraining(true);
    try {
      await trainModel(selectedCity);
      await loadMetrics();
      alert('Model trained successfully!');
    } catch (error) {
      alert('Error training model: ' + error.message);
    } finally {
      setTraining(false);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await predictAQI(selectedCity);
      setPrediction(response.data);
    } catch (error) {
      alert('Error predicting AQI: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCitySearch = async (cityName) => {
    try {
      // Try to predict for the searched city
      // This will trigger the backend to add the city if it doesn't exist
      setLoading(true);
      const response = await predictAQI(cityName);
      setPrediction(response.data);
      
      // Reload cities list to include the new city
      await loadCities();
      
      // Select the new city
      setSelectedCity(cityName);
      
      alert(`City "${cityName}" added successfully!`);
    } catch (error) {
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">AQI Prediction</h1>

        <CitySearch
          cities={cities}
          selectedCity={selectedCity}
          onCityChange={setSelectedCity}
          onCitySearch={handleCitySearch}
        />

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Model Training & Prediction</h3>
          <div className="flex gap-4">
            <button
              onClick={handleTrain}
              disabled={training}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400"
            >
              {training ? 'Training...' : 'Train Model'}
            </button>
            <button
              onClick={handlePredict}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Predicting...' : 'Predict AQI'}
            </button>
          </div>
        </div>

        {prediction && (
          <>
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h2 className="text-2xl font-bold mb-4">Prediction Results</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <p className="text-gray-600 mb-2">Current AQI</p>
                  <p className="text-4xl font-bold">{Math.round(prediction.current_aqi)}</p>
                  <p className={`text-sm ${getAQICategory(prediction.current_aqi).textColor}`}>
                    {getAQICategory(prediction.current_aqi).label}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 mb-2">Predicted AQI (Next Hour)</p>
                  <p className="text-4xl font-bold">{Math.round(prediction.predicted_aqi)}</p>
                  <p className={`text-sm ${getAQICategory(prediction.predicted_aqi).textColor}`}>
                    {getAQICategory(prediction.predicted_aqi).label}
                  </p>
                </div>
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Model: {prediction.model_version}
              </p>
            </div>

            {/* Health Advice Section */}
            <div>
              <h2 className="text-2xl font-bold mb-4">Health Recommendations</h2>
              <AQIHealthAdvice aqi={prediction.predicted_aqi} />
            </div>
          </>
        )}

        {metrics && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Model Performance</h2>
            <p className="mb-4">Best Model: <span className="font-semibold">{metrics.best_model}</span></p>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="px-4 py-2 text-left">Model</th>
                    <th className="px-4 py-2 text-left">MAE</th>
                    <th className="px-4 py-2 text-left">RMSE</th>
                    <th className="px-4 py-2 text-left">R² Score</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(metrics.metrics).map(([model, values]) => (
                    <tr key={model} className="border-b">
                      <td className="px-4 py-2">{model}</td>
                      <td className="px-4 py-2">{values.mae.toFixed(2)}</td>
                      <td className="px-4 py-2">{values.rmse.toFixed(2)}</td>
                      <td className="px-4 py-2">{values.r2.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Prediction;
