export const getAQICategory = (aqi) => {
  if (aqi <= 50) return { label: 'Good', color: 'bg-green-500', textColor: 'text-green-700' };
  if (aqi <= 100) return { label: 'Moderate', color: 'bg-yellow-500', textColor: 'text-yellow-700' };
  if (aqi <= 200) return { label: 'Unhealthy', color: 'bg-orange-500', textColor: 'text-orange-700' };
  if (aqi <= 300) return { label: 'Very Unhealthy', color: 'bg-red-500', textColor: 'text-red-700' };
  return { label: 'Hazardous', color: 'bg-purple-500', textColor: 'text-purple-700' };
};

export const getAQIDescription = (aqi) => {
  if (aqi <= 50) return 'Air quality is satisfactory, and air pollution poses little or no risk.';
  if (aqi <= 100) return 'Air quality is acceptable. However, there may be a risk for some people.';
  if (aqi <= 200) return 'Members of sensitive groups may experience health effects.';
  if (aqi <= 300) return 'Health alert: The risk of health effects is increased for everyone.';
  return 'Health warning of emergency conditions: everyone is more likely to be affected.';
};

export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
