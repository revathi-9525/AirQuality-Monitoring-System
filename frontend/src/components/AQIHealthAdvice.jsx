import React from 'react';

const AQIHealthAdvice = ({ aqi }) => {
  const getHealthAdvice = (aqiValue) => {
    if (aqiValue <= 50) {
      return {
        category: 'Good',
        color: 'bg-green-50 border-green-500',
        textColor: 'text-green-800',
        icon: '😊',
        healthImplications: 'Air quality is satisfactory, and air pollution poses little or no risk.',
        generalPopulation: [
          'Enjoy outdoor activities',
          'Perfect time for exercise and sports',
          'Open windows for fresh air',
          'No precautions needed'
        ],
        sensitiveGroups: [
          'No restrictions for sensitive groups',
          'Safe for children to play outside',
          'Ideal conditions for everyone'
        ],
        recommendations: [
          '✓ Great day for outdoor activities',
          '✓ Go for a walk, jog, or bike ride',
          '✓ Perfect for outdoor sports',
          '✓ Enjoy parks and open spaces'
        ]
      };
    } else if (aqiValue <= 100) {
      return {
        category: 'Moderate',
        color: 'bg-yellow-50 border-yellow-500',
        textColor: 'text-yellow-800',
        icon: '😐',
        healthImplications: 'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.',
        generalPopulation: [
          'Outdoor activities are generally safe',
          'Consider reducing prolonged outdoor exertion',
          'Monitor air quality if planning intense activities',
          'Stay hydrated during outdoor activities'
        ],
        sensitiveGroups: [
          'People with respiratory conditions should limit prolonged outdoor exertion',
          'Children and elderly should take breaks during outdoor activities',
          'Watch for symptoms like coughing or shortness of breath'
        ],
        recommendations: [
          '✓ Outdoor activities are acceptable',
          '⚠ Sensitive individuals should limit prolonged exertion',
          '✓ Keep windows open for ventilation',
          '⚠ Monitor symptoms if you have asthma'
        ]
      };
    } else if (aqiValue <= 150) {
      return {
        category: 'Unhealthy for Sensitive Groups',
        color: 'bg-orange-50 border-orange-500',
        textColor: 'text-orange-800',
        icon: '😷',
        healthImplications: 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.',
        generalPopulation: [
          'Reduce prolonged or heavy outdoor exertion',
          'Take more breaks during outdoor activities',
          'Consider moving activities indoors',
          'Watch for symptoms like coughing or shortness of breath'
        ],
        sensitiveGroups: [
          'Avoid prolonged outdoor exertion',
          'Keep outdoor activities short and light',
          'Consider wearing a mask (N95 or equivalent)',
          'Stay indoors if experiencing symptoms',
          'Keep rescue medications handy if you have asthma'
        ],
        recommendations: [
          '⚠ Limit outdoor activities for sensitive groups',
          '✓ General population can still be active with breaks',
          '⚠ Close windows to prevent outdoor air from coming inside',
          '✓ Use air purifiers indoors',
          '⚠ Wear masks if you must go outside'
        ]
      };
    } else if (aqiValue <= 200) {
      return {
        category: 'Unhealthy',
        color: 'bg-red-50 border-red-500',
        textColor: 'text-red-800',
        icon: '😨',
        healthImplications: 'Everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects.',
        generalPopulation: [
          'Avoid prolonged outdoor exertion',
          'Move activities indoors or reschedule',
          'Reduce physical activity levels',
          'Close windows and doors',
          'Use air purifiers if available'
        ],
        sensitiveGroups: [
          'Avoid all outdoor physical activities',
          'Stay indoors with windows closed',
          'Use air purifiers and keep indoor air clean',
          'Wear N95 masks if you must go outside',
          'Consult your doctor if you have respiratory conditions',
          'Keep medications readily available'
        ],
        recommendations: [
          '❌ Avoid outdoor activities',
          '✓ Stay indoors with windows closed',
          '✓ Use air purifiers',
          '✓ Wear N95 masks if going outside',
          '⚠ Monitor health symptoms closely',
          '✓ Drink plenty of water',
          '⚠ Avoid smoking and exposure to other pollutants'
        ]
      };
    } else if (aqiValue <= 300) {
      return {
        category: 'Very Unhealthy',
        color: 'bg-purple-50 border-purple-500',
        textColor: 'text-purple-800',
        icon: '😱',
        healthImplications: 'Health alert: The risk of health effects is increased for everyone.',
        generalPopulation: [
          'Avoid all outdoor physical activities',
          'Stay indoors with windows and doors closed',
          'Use air purifiers on high settings',
          'Wear N95 masks if you must go outside',
          'Limit indoor physical activities as well'
        ],
        sensitiveGroups: [
          'Remain indoors and keep activity levels low',
          'Follow tips for keeping particle levels low indoors',
          'Wear N95 masks even for brief outdoor exposure',
          'Seek medical attention if experiencing symptoms',
          'Have emergency medications ready',
          'Consider relocating temporarily if possible'
        ],
        recommendations: [
          '❌ Stay indoors - avoid all outdoor activities',
          '✓ Keep windows and doors sealed',
          '✓ Use HEPA air purifiers',
          '✓ Wear N95/P100 masks if going outside',
          '⚠ Seek medical help if experiencing symptoms',
          '✓ Create a clean room with air purifier',
          '❌ Avoid cooking that produces smoke or fumes',
          '✓ Stay hydrated and rest'
        ]
      };
    } else {
      return {
        category: 'Hazardous',
        color: 'bg-red-100 border-red-700',
        textColor: 'text-red-900',
        icon: '☠️',
        healthImplications: 'Health warning of emergency conditions: everyone is more likely to be affected.',
        generalPopulation: [
          'Remain indoors at all times',
          'Keep all windows and doors closed',
          'Use air purifiers continuously',
          'Avoid any physical exertion',
          'Wear N95/P100 masks if evacuation is necessary',
          'Consider evacuation if conditions persist'
        ],
        sensitiveGroups: [
          'Stay indoors in a sealed environment',
          'Use multiple air purifiers',
          'Seek immediate medical attention if experiencing symptoms',
          'Have emergency plan ready',
          'Consider immediate relocation',
          'Keep emergency contacts readily available'
        ],
        recommendations: [
          '🚨 EMERGENCY: Stay indoors at all times',
          '❌ Do NOT go outside unless absolutely necessary',
          '✓ Seal windows and doors completely',
          '✓ Run air purifiers on maximum',
          '🚨 Seek medical help immediately if experiencing symptoms',
          '✓ Create a clean room with sealed doors',
          '❌ Avoid all physical activities',
          '✓ Consider evacuation if possible',
          '🚨 Follow official emergency guidelines'
        ]
      };
    }
  };

  const advice = getHealthAdvice(aqi);

  return (
    <div className={`${advice.color} border-l-4 rounded-lg p-6 mb-6`}>
      <div className="flex items-center mb-4">
        <span className="text-4xl mr-3">{advice.icon}</span>
        <div>
          <h3 className={`text-2xl font-bold ${advice.textColor}`}>
            {advice.category} Air Quality
          </h3>
          <p className="text-sm text-gray-600 mt-1">AQI: {Math.round(aqi)}</p>
        </div>
      </div>

      <div className="space-y-4">
        {/* Health Implications */}
        <div>
          <h4 className={`font-semibold ${advice.textColor} mb-2`}>
            📋 Health Implications
          </h4>
          <p className="text-gray-700">{advice.healthImplications}</p>
        </div>

        {/* General Population */}
        <div>
          <h4 className={`font-semibold ${advice.textColor} mb-2`}>
            👥 For General Population
          </h4>
          <ul className="list-disc list-inside space-y-1 text-gray-700">
            {advice.generalPopulation.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

        {/* Sensitive Groups */}
        <div>
          <h4 className={`font-semibold ${advice.textColor} mb-2`}>
            ⚠️ For Sensitive Groups (Children, Elderly, Respiratory Conditions)
          </h4>
          <ul className="list-disc list-inside space-y-1 text-gray-700">
            {advice.sensitiveGroups.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div>
          <h4 className={`font-semibold ${advice.textColor} mb-2`}>
            💡 Recommendations
          </h4>
          <div className="space-y-1 text-gray-700">
            {advice.recommendations.map((item, index) => (
              <div key={index} className="flex items-start">
                <span className="mr-2">{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Additional Tips */}
        <div className="bg-white bg-opacity-50 rounded p-4 mt-4">
          <h4 className={`font-semibold ${advice.textColor} mb-2`}>
            🏥 Additional Health Tips
          </h4>
          <ul className="list-disc list-inside space-y-1 text-gray-700 text-sm">
            <li>Stay hydrated - drink plenty of water</li>
            <li>Eat antioxidant-rich foods (fruits and vegetables)</li>
            <li>Avoid smoking and secondhand smoke</li>
            <li>Keep indoor plants to help purify air</li>
            <li>Monitor local air quality forecasts</li>
            <li>Consult healthcare provider if you have concerns</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AQIHealthAdvice;
