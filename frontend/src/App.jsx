import { useState, useEffect } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";
import Navbar from "./components/Navbar";
import Auth from "./components/Auth";

function App() {
  const [showAuth, setShowAuth] = useState(false);
  const [user, setUser] = useState(null);

  const fetchUserProfile = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch("http://localhost:8000/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else {
        localStorage.removeItem("token");
      }
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  };

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const handleLoginSuccess = () => {
    setShowAuth(false);
    fetchUserProfile();
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <>
      <Navbar onLoginClick={() => setShowAuth(true)} user={user} onLogout={handleLogout} />
      
      {!user ? (
        <main className="landing-page">
          <h1>Welcome to QueryAnalyser </h1>
          {/* You can add your hero image or other landing page content here */}
        </main>
      ) : (
        <main className="dashboard-page" style={{ padding: "4rem 2rem", textAlign: "center" }}>
          <h1>Dashboard</h1>
          <p>Welcome back, {user.Name}!</p>
          <div style={{ marginTop: "2rem", padding: "2rem", border: "1px dashed #ccc", borderRadius: "8px" }}>
            <p>Your content will go here.</p>
          </div>
        </main>
      )}

      {showAuth && <Auth onClose={() => setShowAuth(false)} onLoginSuccess={handleLoginSuccess} />}
    </>
  );
}

export default App;
