import React, { useEffect, useState } from 'react';
import { heroImage } from '../mock';
import { ChevronDown } from 'lucide-react';

const Hero = ({ onScrollNext }) => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const img = new Image();
    img.src = heroImage;
    img.onload = () => setLoaded(true);
  }, []);

  return (
    <section className="relative h-screen w-full overflow-hidden bg-[#1a1e12]">
      {/* Background image with parallax */}
      <div
        className={`absolute inset-0 bg-cover bg-center transition-all duration-[2000ms] ease-out ${
          loaded ? 'opacity-100 scale-100' : 'opacity-0 scale-105'
        }`}
        style={{ backgroundImage: `url(${heroImage})` }}
      />
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/60" />

      {/* Logo center */}
      <div className="relative z-10 h-full flex flex-col items-center justify-center px-6">
        <div
          className={`text-center transition-all duration-1000 ease-out ${
            loaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="text-[#f2e8cf] text-[10px] md:text-xs tracking-[0.55em] mb-3 md:mb-4 opacity-90">
            MMXXV
          </div>
          <h1 className="vino-display text-[#f2e8cf] text-[80px] md:text-[140px] leading-none tracking-[0.05em]">
            VINO
          </h1>
          <div className="vino-script text-[#f2e8cf] text-2xl md:text-3xl mt-2 md:mt-4 opacity-95">
            by tonino
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <button
        onClick={onScrollNext}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-[#f2e8cf]/80 hover:text-[#f2e8cf] transition-colors flex flex-col items-center gap-2 group"
        aria-label="Scroll down"
      >
        <div className="h-12 w-px bg-[#f2e8cf]/50 group-hover:bg-[#f2e8cf] transition-colors" />
        <ChevronDown size={18} strokeWidth={1.2} className="animate-bounce-slow" />
      </button>
    </section>
  );
};

export default Hero;
