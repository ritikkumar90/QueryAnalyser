import React, { useState } from "react";
import "./Auth.css";

export default function Auth({ onClose }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const url = isLogin
      ? "http://localhost:8000/auth/login"
      : "http://localhost:8000/auth/signup";
    const payload = isLogin ? { email, password } : { name, email, password };

    let header = {};
    let body = {};

    if (isLogin) {
      header = {
        "content-type": "application/x-www-form-urlencoded",
      };
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);
      body = formData;
    } else {
      header = {
        "content-type": "application/json",
      };
      body = JSON.stringify(payload);
    }
    try {
      const response = await fetch(url, {
        method: "post",
        headers: header,
        body: body,
      });

      const data = await response.json();

      if (response.ok) {
        console.log("success: ", data);
      } else {
        console.log("Error form  backend", data);
      }
    } catch (error) {
      console.error("Network error", error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>
        <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>
        <p className="auth-subtitle">
          {isLogin
            ? "Enter your details to access your account"
            : "Sign up to get started with QueryAnalyser"}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="auth-submit">
            {isLogin ? "Sign In" : "Sign Up"}
          </button>
        </form>

        <div className="auth-toggle">
          <span>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
          </span>
          <button className="toggle-btn" onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? "Sign Up" : "Log In"}
          </button>
        </div>
      </div>
    </div>
  );
}
