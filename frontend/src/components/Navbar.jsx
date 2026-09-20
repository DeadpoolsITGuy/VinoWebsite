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
    { label: 'Wine', id: 'wine' },
    { label: 'Contact', id: 'contact' },
  ];

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-40 transition-all duration-500 ${
          scrolled ? 'bg-[#1f2416]/85 backdrop-blur-md py-3' : 'bg-transparent py-6'
        }`}
      >
        <div className="max-w-[1600px] mx-auto px-6 md:px-12 flex items-center justify-between">
          <button
            onClick={() => setOpen(true)}
            className="text-[#f2e8cf] hover:opacity-70 transition-opacity flex items-center gap-2"
            aria-label="Open menu"
          >
            <Menu size={22} strokeWidth={1.4} />
          </button>

          <button
            onClick={() => onNavigate && onNavigate('top')}
            className="text-[#f2e8cf] text-xs tracking-[0.35em] uppercase hover:opacity-70 transition-opacity"
          >
            Vino <span className="font-serif italic tracking-normal normal-case">by tonino</span>
          </button>

          <button
            className="text-[#f2e8cf] hover:opacity-70 transition-opacity flex items-center gap-2 text-xs tracking-[0.25em]"
            aria-label="Cart"
          >
            <ShoppingBag size={18} strokeWidth={1.4} />
            <span className="hidden md:inline">0</span>
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
          className={`absolute inset-0 bg-black/50 transition-opacity duration-500 ${
            open ? 'opacity-100' : 'opacity-0'
          }`}
          onClick={() => setOpen(false)}
        />
        <div
          className={`absolute top-0 left-0 h-full w-[85%] max-w-[380px] bg-[#1f2416] shadow-2xl transition-transform duration-500 ease-out ${
            open ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <div className="flex items-center justify-between p-6 border-b border-[#f2e8cf]/10">
            <span className="text-[#f2e8cf] text-[10px] tracking-[0.4em] uppercase">Menu</span>
            <button onClick={() => setOpen(false)} className="text-[#f2e8cf] hover:opacity-70">
              <X size={22} strokeWidth={1.4} />
            </button>
          </div>
          <nav className="flex flex-col p-8 gap-6">
            {links.map((l) => (
              <button
                key={l.id}
                onClick={() => {
                  onNavigate && onNavigate(l.id);
                  setOpen(false);
                }}
                className="text-left text-[#f2e8cf] text-2xl font-serif hover:italic hover:tracking-wide transition-all"
              >
                {l.label}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </>
  );
};

export default Navbar;
