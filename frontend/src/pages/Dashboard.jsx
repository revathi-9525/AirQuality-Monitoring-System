import React, { useState, useEffect } from 'react';
import { getCities, getCurrentAQI, getAQIHistory } from '../services/api';
import AQICard from '../components/AQICard';
import PollutantChart from '../components/PollutantChart';
import HistoricalChart from '../components/HistoricalChart';
import CitySearch from '../components/CitySearch';

const Dashboard = () => {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [currentAQI, setCurrentAQI] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCities();
  }, []);

  useEffect(() => {
    if (selectedCity) {
      loadCityData();
    }
  }, [selectedCity]);

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

  const loadCityData = async () => {
    setLoading(true);
    try {
      const [aqiResponse, historyResponse] = await Promise.all([
        getCurrentAQI(selectedCity),
        getAQIHistory(selectedCity, 7)
      ]);
      setCurrentAQI(aqiResponse.data);
      setHistory(historyResponse.data);
    } catch (error) {
      console.error('Error loading city data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCitySearch = async (cityName) => {
    try {
      // Try to get current AQI for the searched city
      // This will trigger the backend to add the city if it doesn't exist
      await getCurrentAQI(cityName);
      
      // Reload cities list to include the new city
      await loadCities();
      
      // Select the new city
      setSelectedCity(cityName);
      
      alert(`City "${cityName}" added successfully!`);
    } catch (error) {
      alert(`Error adding city: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
        
        <CitySearch
          cities={cities}
          selectedCity={selectedCity}
          onCityChange={setSelectedCity}
          onCitySearch={handleCitySearch}
        />
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : currentAQI ? (
          <div className="space-y-6">
            <AQICard aqi={currentAQI.aqi} cityName={selectedCity} />
            <div className="grid md:grid-cols-2 gap-6">
              <PollutantChart data={currentAQI} />
              {history.length > 0 && <HistoricalChart data={history} />}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default Dashboard;
