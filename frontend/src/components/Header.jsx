import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold">AirVision AI</Link>
          <nav className="flex gap-6">
            <Link to="/" className="hover:text-blue-200 transition">Home</Link>
            <Link to="/dashboard" className="hover:text-blue-200 transition">Dashboard</Link>
            <Link to="/prediction" className="hover:text-blue-200 transition">Prediction</Link>
            <Link to="/analytics" className="hover:text-blue-200 transition">Analytics</Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
