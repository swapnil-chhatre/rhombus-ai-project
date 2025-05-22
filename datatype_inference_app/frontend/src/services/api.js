// src/services/api.js
import axios from 'axios';

// Base URL for the API
const API_BASE_URL = 'http://localhost:3000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// File upload service
export const uploadFile = async (file, applyInferredTypes = false) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('apply_inferred_types', applyInferredTypes);

    // const response = await apiClient.post('/data_inference/upload/', formData);
    const response = await fetch("http://localhost:8000/api/data_inference/upload/", {
      method: "POST",
      body: formData,
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

// Apply custom types to a processed file
export const applyCustomTypes = async (fileId, columnTypes) => {
  try {
    const response = await apiClient.post(`/data_inference/${fileId}/apply-types/`, 
      { column_types: columnTypes },
      { headers: { 'Content-Type': 'application/json' } }
    );
    return response.data;
  } catch (error) {
    console.error('Error applying custom types:', error);
    throw error;
  }
};

// Download processed file
export const downloadProcessedFile = (url) => {
  window.open(`http://localhost:8000${url}`, '_blank');
};