import React, { useState, useEffect } from 'react';
import { Menu, ShoppingBag, X } from 'lucide-react';

const Navbar = ({ onNavigate }) => {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', handler);
    return () => window.removeEventListener('scroll', handler);
  }, []);

  const links = [
    { label: 'Wine List', id: 'wine' },
    { label: 'Say hello', id: 'contact' },
    { label: 'Instagram', href: 'https://www.instagram.com/vinobytonino/' },
  ];

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-40 transition-all duration-500 ${
          scrolled ? 'bg-foresta/90 backdrop-blur-md py-3' : 'bg-transparent py-6'
        }`}
      >
        <div className="max-w-[1600px] mx-auto px-6 md:px-12 flex items-center justify-between">
          <button
            onClick={() => setOpen(true)}
            className="text-bianco hover:text-ruggine transition-colors flex items-center gap-2"
            aria-label="Open menu"
          >
            <Menu size={22} strokeWidth={1.6} />
            <span className="hidden md:inline vino-mono-medium text-[11px] tracking-[0.3em] uppercase">Menu</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('top')}
            className="text-bianco hover:opacity-80 transition-opacity flex items-baseline gap-2"
          >
            <span className="vino-display text-sm md:text-base tracking-[0.35em]">VINO</span>
            <span className="vino-script text-base md:text-lg">by tonino</span>
          </button>

          <button
            className="text-bianco hover:text-ruggine transition-colors flex items-center gap-2"
            aria-label="Cart"
          >
            <ShoppingBag size={18} strokeWidth={1.6} />
            <span className="hidden md:inline vino-mono-medium text-[11px] tracking-[0.3em]">0</span>
          </button>
        </div>
      </header>

      {/* Slide-in menu */}
      <div
        className={`fixed inset-0 z-50 transition-all duration-500 ${
          open ? 'pointer-events-auto' : 'pointer-events-none'
        }`}
      >
        <div
          className={`absolute inset-0 bg-black/60 transition-opacity duration-500 ${
            open ? 'opacity-100' : 'opacity-0'
          }`}
          onClick={() => setOpen(false)}
        />
        <div
          className={`absolute top-0 left-0 h-full w-[85%] max-w-[400px] bg-foresta shadow-2xl transition-transform duration-500 ease-out ${
            open ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <div className="flex items-center justify-between p-6 border-b border-bianco/10">
            <span className="vino-mono-medium text-bianco text-[10px] tracking-[0.4em] uppercase">Menu</span>
            <button onClick={() => setOpen(false)} className="text-bianco hover:text-ruggine transition-colors">
              <X size={22} strokeWidth={1.6} />
            </button>
          </div>
          <nav className="flex flex-col p-8 gap-6">
            {links.map((l, i) =>
              l.href ? (
                <a
                  key={i}
                  href={l.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => setOpen(false)}
                  className="text-left text-bianco text-2xl vino-display-lite hover:text-ruggine transition-colors"
                >
                  {l.label}
                </a>
              ) : (
                <button
                  key={i}
                  onClick={() => {
                    onNavigate && onNavigate(l.id);
                    setOpen(false);
                  }}
                  className="text-left text-bianco text-2xl vino-display-lite hover:text-ruggine transition-colors"
                >
                  {l.label}
                </button>
              )
            )}
          </nav>
          <div className="absolute bottom-8 left-8 right-8 text-bianco/60">
            <div className="vino-mono text-[10px] tracking-[0.3em] uppercase mb-2">Since MMXXV</div>
            <div className="vino-mono text-[11px]">59 Kempock St, Gourock</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;
