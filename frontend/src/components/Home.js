// frontend/src/components/Home.js
import React, { useState } from 'react';
import axios from 'axios';
import Header from './Header';
import Footer from './Footer';
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
      <Header />
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

      <div>
        <h3>Results</h3>
        {results && (
          <div>
            {results.alt_text.length > 0 && (
              <div>
                <h4>Alt Text Issues</h4>
                <ul>
                  {results.alt_text.map((result, index) => (
                    <li key={index}>
                      <p><strong>Issue:</strong> {result.message}</p>
                      <p><strong>Tag:</strong> {result.tag}</p>
                      <p><strong>WCAG Guideline:</strong> {result.wcag_guideline}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {results.heading_structure.length > 0 && (
              <div>
                <h4>Heading Structure Issues</h4>
                <ul>
                  {results.heading_structure.map((result, index) => (
                    <li key={index}>
                      <p><strong>Issue:</strong> {result.message}</p>
                      <p><strong>Tag:</strong> {result.tag}</p>
                      <p><strong>WCAG Guideline:</strong> {result.wcag_guideline}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};

export default Home;
