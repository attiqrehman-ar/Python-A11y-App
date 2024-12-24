// frontend/src/components/Footer.js
import React from 'react';

const Footer = () => {
  return (
    <footer style={footerStyles}>
      <p>&copy; 2024 WCAG Accessibility Checker. All rights reserved.</p>
    </footer>
  );
};

const footerStyles = {
  backgroundColor: '#333',
  color: 'white',
  padding: '10px',
  textAlign: 'center',
  fontFamily: 'Arial, sans-serif',
  position: 'fixed',
  width: '100%',
  bottom: 0,
};

export default Footer;
