import { useState } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";
import Navbar from "./components/Navbar";
import Auth from "./components/Auth";

function App() {
  const [count, setCount] = useState(0);
  const [showAuth, setShowAuth] = useState(false);

  return (
    <>
      <Navbar onLoginClick={() => setShowAuth(true)} />
      <h1>Welcome to QueryAnalyser </h1>
      {showAuth && <Auth onClose={() => setShowAuth(false)} />}
    </>
  );
}

export default App;
