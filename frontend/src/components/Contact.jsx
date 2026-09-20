import React from 'react';
import { Instagram, Mail, MapPin, Clock } from 'lucide-react';

const DEFAULT_HOURS = [
  { day: 'Wednesday', time: '2pm–late' },
  { day: 'Thursday', time: '2pm–late' },
  { day: 'Friday', time: '12–late' },
  { day: 'Saturday', time: '12–late' },
  { day: 'Sunday', time: '2–late' },
];

const CONTACT = {
  address: ['59 Kempock St', 'Gourock', 'PA19 1NF'],
  email: 'vino@toninos.co.uk',
  instagram: 'https://www.instagram.com/vinobytonino/',
};

const Contact = React.forwardRef(({ siteConfig }, ref) => {
  const hours =
    siteConfig?.hours && siteConfig.hours.length > 0 ? siteConfig.hours : DEFAULT_HOURS;

  return (
    <section ref={ref} id="contact" className="relative bg-foresta py-12 md:py-16 px-6">
      <div className="max-w-[1400px] mx-auto">
        <div className="flex items-center gap-3 justify-center mb-6">
          <div className="h-px w-10 bg-ruggine" />
          <span className="vino-mono-medium text-ruggine text-[10px] md:text-xs tracking-[0.4em]">SAY CIAO</span>
          <div className="h-px w-10 bg-ruggine" />
        </div>
        <h2 className="vino-display text-bianco text-4xl md:text-7xl text-center tracking-[0.1em] mb-6">
          GET IN TOUCH
        </h2>
        <p className="vino-mono text-center text-[11px] md:text-[12px] tracking-[0.15em] text-bianco/80 mb-12">
          It all begins with a glass of vino.
        </p>
        <div className="h-px w-full bg-bianco/25 mb-14" />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8 text-center">
          <div>
            <div className="flex justify-center mb-4 text-ruggine">
              <MapPin size={18} strokeWidth={1.6} />
            </div>
            <div className="vino-mono-medium text-[11px] tracking-[0.4em] text-bianco mb-5">ADDRESS</div>
            <div className="vino-mono text-[12px] text-bianco/90 space-y-1">
              {CONTACT.address.map((line, i) => (
                <div key={i}>{line}</div>
              ))}
            </div>
          </div>

          <div>
            <div className="flex justify-center mb-4 text-ruggine">
              <Clock size={18} strokeWidth={1.6} />
            </div>
            <div className="vino-mono-medium text-[11px] tracking-[0.4em] text-bianco mb-5">HOURS</div>
            <div className="vino-mono text-[12px] text-bianco/90 space-y-1">
              {hours.map((h, i) => (
                <div key={i}>
                  {h.day} {h.time}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="flex justify-center mb-4 text-ruggine">
              <Mail size={18} strokeWidth={1.6} />
            </div>
            <div className="vino-mono-medium text-[11px] tracking-[0.4em] text-bianco mb-5">EMAIL</div>
            <a
              href={`mailto:${CONTACT.email}`}
              className="vino-mono text-[12px] text-bianco/90 underline underline-offset-4 hover:text-ruggine transition-colors"
            >
              {CONTACT.email}
            </a>
          </div>
        </div>

        <div className="flex justify-center mt-16">
          <a
            href={CONTACT.instagram}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 vino-mono-medium text-[12px] tracking-[0.25em] text-bianco hover:text-ruggine underline underline-offset-4 transition-colors"
          >
            <Instagram size={16} strokeWidth={1.6} />
            INSTAGRAM
          </a>
        </div>

        <div className="mt-20 flex flex-col items-center gap-4">
          <div className="vino-display text-bianco text-2xl tracking-[0.35em]">VINO</div>
          <div className="vino-script text-bianco/80 text-lg -mt-2">by tonino</div>
          <div className="vino-mono text-[10px] tracking-[0.3em] text-bianco/50">
            © {new Date().getFullYear()} · GOUROCK · SCOTLAND
          </div>
        </div>
      </div>
    </section>
  );
});

export default Contact;
