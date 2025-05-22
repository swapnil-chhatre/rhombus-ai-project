// src/components/common/Spinner.js
import React from 'react';
import './Spinner.css';

const Spinner = () => {
  return (
    <div className="spinner-overlay">
      <div className="spinner"></div>
      <p>Processing...</p>
    </div>
  );
};

export default Spinner;