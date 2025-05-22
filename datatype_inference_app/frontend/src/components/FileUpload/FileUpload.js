// src/components/FileUpload/FileUpload.js
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFile } from '../../services/api';
import { useDataContext } from '../../contexts/DataContext';
import './FileUpload.css';

const FileUpload = () => {
  const {
    setFileData,
    setIsLoading,
    setError
  } = useDataContext();
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [applyTypes, setApplyTypes] = useState(false);
  
  // Setup dropzone for file upload
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
      }
    },
  });
  
  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      // Call API to upload and process the file
      const data = await uploadFile(selectedFile, applyTypes);
      
      // Update state with the processed data
      setFileData(data);
      
      // Reset selected file
      setSelectedFile(null);
    } catch (error) {
      setError(error.response?.data?.error || 'Error uploading file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="file-upload-container">
      <h2>Upload Dataset</h2>
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the file here...</p>
        ) : (
          <p>Drag & drop a CSV or Excel file here, or click to select a file</p>
        )}
      </div>
      
      {selectedFile && (
        <div className="selected-file">
          <p>Selected file: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)</p>
        </div>
      )}
      
      <div className="options">
        <label>
          <input
            type="checkbox"
            checked={applyTypes}
            onChange={(e) => setApplyTypes(e.target.checked)}
          />
          Automatically apply inferred data types
        </label>
      </div>
      
      <button 
        className="upload-button"
        onClick={handleUpload}
        disabled={!selectedFile}
      >
        Process File
      </button>
    </div>
  );
};

export default FileUpload;