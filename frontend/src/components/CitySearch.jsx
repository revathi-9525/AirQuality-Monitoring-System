import React, { useState, useEffect } from 'react';

const CitySearch = ({ cities, selectedCity, onCityChange, onCitySearch }) => {
  const [searchInput, setSearchInput] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async () => {
    if (!searchInput.trim()) {
      alert('Please enter a city name');
      return;
    }
    
    setIsSearching(true);
    try {
      await onCitySearch(searchInput.trim());
      setSearchInput('');
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <div className="grid md:grid-cols-2 gap-4">
        {/* Dropdown for existing cities */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select from existing cities
          </label>
          <select
            value={selectedCity}
            onChange={(e) => onCityChange(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {cities.map((city) => (
              <option key={city.id} value={city.name}>
                {city.name}, {city.country}
              </option>
            ))}
          </select>
        </div>

        {/* Search input for new cities */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or search for any city
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter city name (e.g., Paris, Tokyo)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isSearching}
            />
            <button
              onClick={handleSearch}
              disabled={isSearching}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              {isSearching ? (
                <span className="flex items-center">
                  <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Searching...
                </span>
              ) : (
                'Search'
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Search any city worldwide - it will be added automatically
          </p>
        </div>
      </div>
    </div>
  );
};

export default CitySearch;
