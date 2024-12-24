import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [url, setUrl] = useState('');
  const [results, setResults] = useState({});

  // Helper function to call the new API
  const checkAccessibility = () => {
    axios
      .post('http://127.0.0.1:5000/api/check-url-accessibility', { url })
      .then(response => {
        setResults(response.data);  // Update the results with the API response
      })
      .catch(error => {
        console.error('Error checking accessibility:', error);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    checkAccessibility(); // Call the function to check the URL
  };

  return (
    <div>
      <h1>WCAG Accessibility Checker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter Website URL"
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
