import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [url, setUrl] = useState(''); // For URL input
  const [htmlContent, setHtmlContent] = useState('');
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Helper function to call an API
  const checkAccessibility = async (endpoint, data) => {
    try {
      const response = await axios.post(endpoint, data);
      setResults(prevResults => ({
        ...prevResults,
        [endpoint]: response.data,
      }));
    } catch (err) {
      console.error('Error checking accessibility:', err);
      setError('An error occurred while checking accessibility.');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const requestData = url ? { url } : { html: htmlContent }; // Send URL or HTML content

    const endpoints = [
      'check-alt-text',
      'check-aria-labels',
      'check-color-contrast',
      'check-heading-structure',
      'check-keyboard-navigation'
    ];

    endpoints.forEach(endpoint => checkAccessibility(`http://127.0.0.1:5000/api/${endpoint}`, requestData));

    setLoading(false);
  };

  return (
    <div>
      <h1>WCAG Accessibility Checker</h1>
      <form onSubmit={handleSubmit}>
        {/* Input for URL */}
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <br />
        {/* Fallback for pasting HTML content */}
        <textarea
          rows="10"
          cols="50"
          value={htmlContent}
          onChange={(e) => setHtmlContent(e.target.value)}
          placeholder="Or paste HTML content here"
        />
        <br />
        <button type="submit" disabled={loading}>Check Accessibility</button>
      </form>

      {loading && <p>Checking...</p>}
      {error && <p>{error}</p>}

      <div>
        <h2>Results</h2>
        <pre>{JSON.stringify(results, null, 2)}</pre>
      </div>
    </div>
  );
};

export default Home;
