import React from 'react';
import { contactInfo } from '../mock';
import { Instagram } from 'lucide-react';

const Contact = React.forwardRef((props, ref) => {
  return (
    <section ref={ref} id="contact" className="relative bg-[#252a1a] py-24 md:py-32 px-6">
      <div className="max-w-[1400px] mx-auto">
        <h2 className="vino-display text-[#f2e8cf] text-5xl md:text-7xl text-center tracking-[0.08em] mb-6">
          GET IN TOUCH
        </h2>
        <p className="vino-mono text-center text-[11px] md:text-[12px] tracking-[0.15em] text-[#f2e8cf]/80 mb-12">
          It all begins with a glass of vino.
        </p>
        <div className="h-px w-full bg-[#f2e8cf]/30 mb-14" />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8 text-center">
          <div>
            <div className="vino-mono text-[11px] tracking-[0.35em] text-[#f2e8cf] mb-6">
              ADDRESS
            </div>
            <div className="vino-mono text-[12px] text-[#f2e8cf]/90 space-y-1">
              {contactInfo.address.map((line, i) => (
                <div key={i}>{line}</div>
              ))}
            </div>
          </div>

          <div>
            <div className="vino-mono text-[11px] tracking-[0.35em] text-[#f2e8cf] mb-6">
              HOURS
            </div>
            <div className="vino-mono text-[12px] text-[#f2e8cf]/90 space-y-1">
              {contactInfo.hours.map((h, i) => (
                <div key={i}>
                  {h.day} {h.time}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="vino-mono text-[11px] tracking-[0.35em] text-[#f2e8cf] mb-6">
              EMAIL
            </div>
            <a
              href={`mailto:${contactInfo.email}`}
              className="vino-mono text-[12px] text-[#f2e8cf]/90 underline underline-offset-4 hover:text-[#f2e8cf] transition-colors"
            >
              {contactInfo.email}
            </a>
          </div>
        </div>

        <div className="flex justify-center mt-16">
          <a
            href={contactInfo.instagram}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 vino-mono text-[12px] tracking-[0.2em] text-[#f2e8cf]/90 hover:text-[#f2e8cf] underline underline-offset-4 transition-colors"
          >
            <Instagram size={16} strokeWidth={1.4} />
            Instagram
          </a>
        </div>

        <div className="mt-20 text-center vino-mono text-[10px] tracking-[0.3em] text-[#f2e8cf]/50">
          © {new Date().getFullYear()} VINO BY TONINO · GOUROCK
        </div>
      </div>
    </section>
  );
});

export default Contact;
