import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [htmlContent, setHtmlContent] = useState('');
  const [results, setResults] = useState({});

  // Helper function to call an API
  const checkAccessibility = (endpoint) => {
    axios
      .post(`http://127.0.0.1:5000/api/${endpoint}`, { html: htmlContent })
      .then(response => {
        setResults(prevResults => ({
          ...prevResults,
          [endpoint]: response.data,
        }));
      })
      .catch(error => {
        console.error('Error checking accessibility:', error);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    checkAccessibility('check-alt-text'); // For example, check alt text
    checkAccessibility('check-aria-labels');
    checkAccessibility('check-color-contrast');
    checkAccessibility('check-heading-structure');
    checkAccessibility('check-keyboard-navigation');
  };

  return (
    <div>
      <h1>WCAG Accessibility Checker</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="10"
          cols="50"
          value={htmlContent}
          onChange={(e) => setHtmlContent(e.target.value)}
          placeholder="Paste HTML content here"
        />
        <br />
        <button type="submit">Check Accessibility</button>
      </form>

      <div>
        <h2>Results</h2>
        <pre>{JSON.stringify(results, null, 2)}</pre>
      </div>
    </div>
  );
};

export default Home;
