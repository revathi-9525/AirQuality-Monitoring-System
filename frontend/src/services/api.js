import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ----------------------
// API Calls
// ----------------------

export const getCities = () => api.get("/cities");

export const getCurrentAQI = (cityName) =>
  api.get(`/aqi/${cityName}`);

export const getAQIHistory = (cityName, days = 7) =>
  api.get(`/aqi/history/${cityName}?days=${days}`);

export const trainModel = (cityName) =>
  api.post(`/train-model?city_name=${cityName}`);

export const predictAQI = (cityName) =>
  api.get(`/predict/${cityName}`);

export const getModelMetrics = () =>
  api.get("/model-metrics");

export const getAlerts = (limit = 10) =>
  api.get(`/alerts?limit=${limit}`);

export const configureAlert = (cityName, threshold) =>
  api.post("/alerts/configure", {
    city_name: cityName,
    threshold,
  });

export const refreshAQI = (cityName) =>
  api.post(`/aqi/refresh/${cityName}`);

export const refreshAllAQI = () =>
  api.post("/aqi/refresh-all");

export const generateSampleData = (cityName, hours = 24) =>
  api.post(`/aqi/generate-sample/${cityName}?hours=${hours}`);

export const generateSampleDataAll = (hours = 24) =>
  api.post(`/aqi/generate-sample-all?hours=${hours}`);

export default api;