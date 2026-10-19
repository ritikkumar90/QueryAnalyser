import { useState, useEffect } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Auth from "./components/Auth";
import QueryPage from "./components/QueryPage";

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

      <main>
        <QueryPage />
      </main>

      {showAuth && <Auth onClose={() => setShowAuth(false)} onLoginSuccess={handleLoginSuccess} />}
    </>
  );
}

export default App;
