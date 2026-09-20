import React, { useEffect, useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { resolveAssetUrl } from '../lib/api';

const Hero = ({ onScrollNext, siteConfig }) => {
  const [loaded, setLoaded] = useState(false);
  const heroUrl = resolveAssetUrl(siteConfig?.hero_image_url);

  useEffect(() => {
    if (!heroUrl) return;
    setLoaded(false);
    const img = new Image();
    img.src = heroUrl;
    img.onload = () => setLoaded(true);
    img.onerror = () => setLoaded(true);
  }, [heroUrl]);

  return (
    <section className="relative h-screen w-full overflow-hidden bg-foresta">
      <div
        className={`absolute inset-0 bg-cover bg-center transition-all duration-[1800ms] ease-out ${
          loaded ? 'opacity-100 scale-100' : 'opacity-0 scale-105'
        }`}
        style={{ backgroundImage: `url(${heroUrl})` }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-black/45 via-black/30 to-foresta/70" />

      {/* SINCE 2025 top-left badge */}
      <div className="absolute top-24 md:top-28 left-6 md:left-12 z-10">
        <div className="flex items-center gap-3">
          <div className="h-px w-8 bg-bianco/60" />
          <div className="vino-mono-medium text-bianco/90 text-[10px] tracking-[0.4em]">SINCE 2025</div>
        </div>
      </div>

      {/* Location top-right */}
      <div className="absolute top-24 md:top-28 right-6 md:right-12 z-10 hidden sm:block">
        <div className="flex items-center gap-3">
          <div className="vino-mono-medium text-bianco/90 text-[10px] tracking-[0.4em]">GOUROCK · SCOTLAND</div>
          <div className="h-px w-8 bg-bianco/60" />
        </div>
      </div>

      {/* Logo center */}
      <div className="relative z-10 h-full flex flex-col items-center justify-center px-6">
        <div
          className={`text-center transition-all duration-1000 ease-out ${
            loaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="vino-mono-medium text-bianco text-[11px] md:text-xs tracking-[0.55em] mb-3 md:mb-5 opacity-90">
            {siteConfig?.since_year || 'MMXXV'}
          </div>
          <h1 className="vino-display text-bianco text-[80px] md:text-[160px] leading-none tracking-[0.06em]">
            VINO
          </h1>
          <div className="vino-script text-bianco text-3xl md:text-5xl mt-1 md:mt-2 opacity-95">
            {siteConfig?.hero_tagline || 'by tonino'}
          </div>
        </div>
      </div>

      <button
        onClick={onScrollNext}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-bianco/80 hover:text-bianco transition-colors flex flex-col items-center gap-2 group"
        aria-label="Scroll down"
      >
        <div className="vino-mono-medium text-[10px] tracking-[0.4em] mb-1">EXPLORE</div>
        <div className="h-12 w-px bg-bianco/50 group-hover:bg-bianco transition-colors" />
        <ChevronDown size={18} strokeWidth={1.4} className="animate-bounce-slow" />
      </button>
    </section>
  );
};

export default Hero;
