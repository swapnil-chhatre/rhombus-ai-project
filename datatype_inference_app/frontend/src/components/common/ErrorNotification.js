// src/components/common/ErrorNotification.js
import React from 'react';
import './ErrorNotification.css';

const ErrorNotification = ({ message, onClose }) => {
  return (
    <div className="error-notification">
      <div className="error-content">
        <span className="error-icon">⚠️</span>
        <p>{message}</p>
        <button className="error-close" onClick={onClose}>×</button>
      </div>
    </div>
  );
};

export default ErrorNotification;