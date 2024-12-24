import React, { useState } from 'react';
import axios from 'axios';
import Header from './Header';
import Footer from './Footer';

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

  const handleDownloadPdf = () => {
    if (results) {
      axios
        .post('http://127.0.0.1:5000/api/generate-pdf-report', { results }, { responseType: 'blob' })
        .then((response) => {
          const blob = new Blob([response.data], { type: 'application/pdf' });
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = 'accessibility_report.pdf';
          link.click();
        })
        .catch((error) => {
          setError('Error generating the PDF report.');
        });
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
            <h4>Alt Text Issues</h4>
            {results.alt_text && results.alt_text.length > 0 ? (
              <ul>
                {results.alt_text.map((issue, index) => (
                  <li key={index}>
                    Missing alt attribute for <strong>{issue.tag}</strong> at{' '}
                    <em>{issue.location}</em>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No issues found for Alt Text.</p>
            )}

            <h4>ARIA Labels Issues</h4>
            {results.aria_labels && results.aria_labels.length > 0 ? (
              <ul>
                {results.aria_labels.map((issue, index) => (
                  <li key={index}>
                    ARIA label missing for <strong>{issue.tag}</strong> at{' '}
                    <em>{issue.location}</em>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No issues found for ARIA Labels.</p>
            )}

            <h4>Heading Structure Issues</h4>
            {results.heading_structure && results.heading_structure.length > 0 ? (
              <ul>
                {results.heading_structure.map((issue, index) => (
                  <li key={index}>
                    Skipped heading: <strong>{issue.message}</strong> at{' '}
                    <em>{issue.location}</em>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No issues found for Heading Structure.</p>
            )}

            <button onClick={handleDownloadPdf}>Download PDF Report</button>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};

export default Home;
