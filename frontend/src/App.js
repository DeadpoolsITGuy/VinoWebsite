import React, { useRef } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import WineList from './components/WineList';
import Contact from './components/Contact';

const Home = () => {
  const wineRef = useRef(null);
  const contactRef = useRef(null);

  const handleNavigate = (id) => {
    if (id === 'wine' && wineRef.current) {
      wineRef.current.scrollIntoView({ behavior: 'smooth' });
    } else if (id === 'contact' && contactRef.current) {
      contactRef.current.scrollIntoView({ behavior: 'smooth' });
    } else if (id === 'top') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div className="bg-[#1a1e12] min-h-screen">
      <Navbar onNavigate={handleNavigate} />
      <Hero onScrollNext={() => handleNavigate('wine')} />
      <WineList ref={wineRef} />
      <Contact ref={contactRef} />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
