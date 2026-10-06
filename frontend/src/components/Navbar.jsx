import React from 'react';
import './Navbar.css';

export default function Navbar({ onLoginClick }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <a href="/" className="navbar-logo">
          QueryAnalyser
        </a>
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="/" className="nav-links">Home</a>
          </li>
          <li className="nav-item">
            <a href="/about" className="nav-links">About</a>
          </li>
          <li className="nav-item">
            <a href="/services" className="nav-links">Services</a>
          </li>
          <li className="nav-item">
            <a href="/contact" className="nav-links">Contact</a>
          </li>
          <li className="nav-item">
            <a href="#" className="nav-links login-btn" onClick={(e) => { e.preventDefault(); onLoginClick(); }}>Login</a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
