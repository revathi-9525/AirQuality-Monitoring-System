import React, { useState, useEffect } from 'react';
import { getCities, getAQIHistory, getAlerts, refreshAllAQI, generateSampleDataAll } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatDate } from '../utils/aqiUtils';
import CitySearch from '../components/CitySearch';

const Analytics = () => {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [days, setDays] = useState(7);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    loadCities();
    loadAlerts();
  }, []);

  useEffect(() => {
    if (selectedCity) {
      loadHistory();
    }
  }, [selectedCity, days]);

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

  const loadHistory = async () => {
    try {
      const response = await getAQIHistory(selectedCity, days);
      setHistory(response.data);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const loadAlerts = async () => {
    try {
      const response = await getAlerts(20);
      setAlerts(response.data);
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  const refreshData = async () => {
    setIsRefreshing(true);
    setHistory([]);
    
    try {
      const hoursToGenerate = 720; // Always generate 30 days of data
      
      try {
        await refreshAllAQI();
      } catch (apiError) {
        console.log('API fetch failed, generating sample data...');
        const response = await generateSampleDataAll(hoursToGenerate);
        console.log('Generated:', response.data);
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (selectedCity) {
        await loadHistory();
      }
    } catch (error) {
      console.error('Error refreshing data:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleCitySearch = async (cityName) => {
    try {
      // Try to get history for the searched city
      // This will trigger the backend to add the city if it doesn't exist
      await getAQIHistory(cityName, days);
      
      // Reload cities list to include the new city
      await loadCities();
      
      // Select the new city
      setSelectedCity(cityName);
      
      alert(`City "${cityName}" added successfully!`);
    } catch (error) {
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  const chartData = history.map(item => ({
    time: formatDate(item.timestamp),
    AQI: item.aqi,
    PM2_5: item.pm2_5,
    PM10: item.pm10,
  }));

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Analytics</h1>

        <CitySearch
          cities={cities}
          selectedCity={selectedCity}
          onCityChange={setSelectedCity}
          onCitySearch={handleCitySearch}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">AQI Trends</h2>
            <div className="flex flex-wrap gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Period
                </label>
                <select
                  value={days}
                  onChange={(e) => setDays(Number(e.target.value))}
                  className="px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value={1}>Last 24 Hours</option>
                  <option value={7}>Last 7 Days</option>
                  <option value={30}>Last 30 Days</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={refreshData}
                  disabled={isRefreshing}
                  className={`px-4 py-2 rounded-lg text-white ${
                    isRefreshing ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {isRefreshing ? 'Refreshing...' : 'Refresh Data'}
                </button>
              </div>
            </div>

            {isRefreshing ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-gray-600">Loading data...</p>
              </div>
            ) : history.length > 0 ? (
              <>
                <p className="text-sm text-gray-600 mb-4">
                  Showing {history.length} records from the last {days === 1 ? '24 hours' : days === 7 ? '7 days' : '30 days'}
                </p>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="AQI" stroke="#8b5cf6" strokeWidth={2} />
                    <Line type="monotone" dataKey="PM2_5" stroke="#ef4444" strokeWidth={2} />
                    <Line type="monotone" dataKey="PM10" stroke="#f59e0b" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No data available for the selected period</p>
                <button
                  onClick={refreshData}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Generate Sample Data
                </button>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Recent Alerts</h2>
              <button
                onClick={loadAlerts}
                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                Refresh
              </button>
            </div>
            {alerts.length > 0 ? (
              <div className="space-y-3 max-h-[500px] overflow-y-auto">
                {alerts.map((alert) => {
                  const getAlertColor = (aqi) => {
                    if (aqi >= 300) return 'border-purple-600 bg-purple-50 text-purple-900';
                    if (aqi >= 201) return 'border-red-600 bg-red-50 text-red-900';
                    if (aqi >= 150) return 'border-orange-500 bg-orange-50 text-orange-900';
                    if (aqi >= 101) return 'border-yellow-500 bg-yellow-50 text-yellow-900';
                    return 'border-green-500 bg-green-50 text-green-900';
                  };

                  return (
                    <div
                      key={alert.id}
                      className={`border-l-4 p-3 rounded-r ${getAlertColor(alert.aqi_value)}`}
                    >
                      <p className="font-semibold text-sm">{alert.message}</p>
                      <p className="text-xs mt-1 opacity-75">
                        AQI: {alert.aqi_value?.toFixed(0)} | Threshold: {alert.threshold}
                      </p>
                      <p className="text-xs mt-2 opacity-60">
                        {new Date(alert.created_at).toLocaleString()}
                      </p>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p className="text-gray-600 mt-2">No alerts found</p>
                <p className="text-sm text-gray-500 mt-1">Air quality is within safe limits</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
