// frontend/src/components/Home.js
import React, { useState } from 'react';
import axios from 'axios';
import Header from './Header';
import Footer from './Footer';

const Home = () => {
  const [url, setUrl] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  // Function to fetch results from the backend
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

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) {
      checkAccessibility(url);
    }
  };

  // Function to generate and download the report as PDF
  const generateAndDownloadReport = async (results) => {
    const response = await axios.post('http://127.0.0.1:5000/api/download-report', { results }, {
      responseType: 'blob',  // Set the response type to handle binary data
    });

    // Create a downloadable link for the PDF
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'accessibility_report.pdf';
    link.click();
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
            <button
              onClick={() => generateAndDownloadReport(results)}
              style={{
                padding: '10px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                cursor: 'pointer',
                marginTop: '20px',
              }}
            >
              Download Report as PDF
            </button>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};

export default Home;
