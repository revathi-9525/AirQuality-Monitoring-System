import React from 'react';
import { getAQICategory, getAQIDescription } from '../utils/aqiUtils';

const AQICard = ({ aqi, cityName }) => {
  const category = getAQICategory(aqi);
  const description = getAQIDescription(aqi);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">{cityName}</h2>
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-gray-600 text-sm">Current AQI</p>
          <p className="text-5xl font-bold">{Math.round(aqi)}</p>
        </div>
        <div className={`${category.color} text-white px-6 py-3 rounded-lg`}>
          <p className="text-lg font-semibold">{category.label}</p>
        </div>
      </div>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  );
};

export default AQICard;
