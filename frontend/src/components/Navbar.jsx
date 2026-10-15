import React from 'react';
import './Navbar.css';

export default function Navbar({ onLoginClick, user, onLogout }) {
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
          {!user && (
            <>
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
            </>
          )}
          {user && (
            <>
              <li className="nav-item">
                <span className="nav-links" style={{ fontWeight: "bold" }}>Hi, {user.Name}</span>
              </li>
              <li className="nav-item">
                <a href="#" className="nav-links login-btn" onClick={(e) => { e.preventDefault(); onLogout(); }}>Logout</a>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}
