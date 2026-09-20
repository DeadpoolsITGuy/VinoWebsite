import React, { useEffect, useRef, useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import WineList from './components/WineList';
import Contact from './components/Contact';
import Admin from './pages/Admin';
import { getMenu, getSiteConfig } from './lib/api';

const Home = () => {
  const wineRef = useRef(null);
  const contactRef = useRef(null);
  const [menu, setMenu] = useState(null);
  const [siteConfig, setSiteConfig] = useState(null);

  useEffect(() => {
    getMenu().then(setMenu).catch(() => {});
    getSiteConfig().then(setSiteConfig).catch(() => {});
  }, []);

  const handleNavigate = (id) => {
    if (id === 'wine' && wineRef.current) wineRef.current.scrollIntoView({ behavior: 'smooth' });
    else if (id === 'contact' && contactRef.current) contactRef.current.scrollIntoView({ behavior: 'smooth' });
    else if (id === 'top') window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="bg-foresta min-h-screen">
      <Navbar onNavigate={handleNavigate} />
      <Hero onScrollNext={() => handleNavigate('wine')} siteConfig={siteConfig} />
      <WineList ref={wineRef} menu={menu} />
      <Contact ref={contactRef} siteConfig={siteConfig} />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
