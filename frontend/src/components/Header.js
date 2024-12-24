// frontend/src/components/Header.js
import React from 'react';

const Header = () => {
  return (
    <header style={headerStyles}>
      <h1>WCAG Accessibility Checker</h1>
    </header>
  );
};

const headerStyles = {
  backgroundColor: '#4CAF50',
  color: 'white',
  padding: '20px',
  textAlign: 'center',
  fontFamily: 'Arial, sans-serif',
};

export default Header;
