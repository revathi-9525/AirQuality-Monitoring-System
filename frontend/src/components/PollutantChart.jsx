import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PollutantChart = ({ data }) => {
  const chartData = [
    { name: 'PM2.5', value: data.pm2_5 },
    { name: 'PM10', value: data.pm10 },
    { name: 'NO2', value: data.no2 },
    { name: 'SO2', value: data.so2 },
    { name: 'CO', value: data.co },
    { name: 'O3', value: data.o3 },
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold mb-4">Pollutant Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PollutantChart;
