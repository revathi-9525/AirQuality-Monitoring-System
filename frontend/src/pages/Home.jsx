import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">AirVision AI</h1>
          <p className="text-xl text-gray-600 mb-8">Intelligent Air Quality Monitoring & Forecasting System</p>
          <Link to="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition inline-block">
            View Dashboard
          </Link>
        </div>
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Real-Time Monitoring</h3>
            <p className="text-gray-600">Track air quality metrics in real-time with live data updates.</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold mb-2">AI Predictions</h3>
            <p className="text-gray-600">Advanced ML models predict future AQI levels with high accuracy.</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-4xl mb-4">🔔</div>
            <h3 className="text-xl font-bold mb-2">Smart Alerts</h3>
            <p className="text-gray-600">Get notified when air quality reaches unhealthy levels.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
