// src/App.js (updated)
import React from 'react';
import { DataProvider, useDataContext } from './contexts/DataContext';
import FileUpload from './components/FileUpload/FileUpload';
import Spinner from './components/common/Spinner';
import ErrorNotification from './components/common/ErrorNotification';
import './App.css';

// Main content component
const MainContent = () => {
  const { isLoading, error, setError } = useDataContext();
  
  return (
    <>
      <FileUpload />
      {/* More components will be added here in future steps */}
      
      {isLoading && <Spinner />}
      {error && (
        <ErrorNotification 
          message={error} 
          onClose={() => setError(null)} 
        />
      )}
    </>
  );
};

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Data Type Inference Tool</h1>
      </header>
      <main>
        <DataProvider>
          <MainContent />
        </DataProvider>
      </main>
      <footer>
        <p>Data Type Inference Web Application - Created with React & Django</p>
      </footer>
    </div>
  );
}

export default App;