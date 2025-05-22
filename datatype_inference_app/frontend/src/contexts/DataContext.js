// src/contexts/DataContext.js
import React, { createContext, useState, useContext } from 'react';

// Create the context
const DataContext = createContext();

// Custom hook for using the context
export const useDataContext = () => useContext(DataContext);

// Provider component
export const DataProvider = ({ children }) => {
  // State for the uploaded file data
  const [fileData, setFileData] = useState(null);
  
  // State for the processed file information
  const [processedFile, setProcessedFile] = useState(null);
  
  // State for loading indicators
  const [isLoading, setIsLoading] = useState(false);
  
  // State for error messages
  const [error, setError] = useState(null);
  
  // State for custom type selections by the user
  const [customTypes, setCustomTypes] = useState({});
  
  // Function to update a column's custom type
  const updateColumnType = (columnName, newType) => {
    setCustomTypes(prev => ({
      ...prev,
      [columnName]: newType
    }));
  };
  
  // Function to reset the application state
  const resetState = () => {
    setFileData(null);
    setProcessedFile(null);
    setError(null);
    setCustomTypes({});
  };
  
  // Value object to be provided to consumers
  const value = {
    fileData,
    setFileData,
    processedFile,
    setProcessedFile,
    isLoading,
    setIsLoading,
    error,
    setError,
    customTypes,
    updateColumnType,
    resetState
  };
  
  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};