// frontend/src/components/Home.js
import React, { useState } from 'react';
import axios from 'axios';
import Header from './Header'; // Add this line
import Footer from './Footer'; // Add this line
import Results from './Results';

const Home = () => {
  const [url, setUrl] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const checkAccessibility = (url) => {
    axios
      .post('http://127.0.0.1:5000/api/check-url-accessibility', { url })
      .then(response => {
        setResults(response.data);
        setError('');
      })
      .catch(error => {
        setResults(null);
        setError('Error fetching results from the server.');
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) {
      checkAccessibility(url);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <Header /> {/* Header component */}
      <div style={{ margin: '20px 0' }}>
        <h2>Enter Website URL</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter Website URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ padding: '10px', width: '300px', marginRight: '10px' }}
          />
          <button
            type="submit"
            style={{
              padding: '10px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            Check Accessibility
          </button>
        </form>
      </div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <Results results={results} />
      <Footer /> {/* Footer component */}
    </div>
  );
};

export default Home;
