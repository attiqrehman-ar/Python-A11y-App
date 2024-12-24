// frontend/src/components/Results.js
import React from 'react';

const Results = ({ results }) => {
  return (
    <div style={resultsStyles}>
      {results ? (
        <>
          {results.alt_text && (
            <div>
              <h3>Alt Text Results</h3>
              <pre>{JSON.stringify(results.alt_text, null, 2)}</pre>
            </div>
          )}
          {results.aria_labels && (
            <div>
              <h3>ARIA Labels Results</h3>
              <pre>{JSON.stringify(results.aria_labels, null, 2)}</pre>
            </div>
          )}
          {results.heading_structure && (
            <div>
              <h3>Heading Structure Results</h3>
              <pre>{JSON.stringify(results.heading_structure, null, 2)}</pre>
            </div>
          )}
        </>
      ) : (
        <p>No results to display</p>
      )}
    </div>
  );
};

const resultsStyles = {
  padding: '20px',
  marginTop: '20px',
  border: '1px solid #ccc',
  backgroundColor: '#f9f9f9',
  fontFamily: 'Arial, sans-serif',
};

export default Results;
