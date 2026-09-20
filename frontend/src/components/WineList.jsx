import React from 'react';
import { wineData } from '../mock';

const WineRow = ({ name, price }) => (
  <div className="flex items-baseline gap-4 py-2 group">
    <span className="vino-mono text-[11px] md:text-[12px] text-[#f2e8cf]/90 leading-relaxed flex-1 group-hover:text-[#f2e8cf] transition-colors">
      {name}
    </span>
    <span className="vino-mono text-[11px] md:text-[12px] text-[#f2e8cf]/80 whitespace-nowrap">
      {price}
    </span>
  </div>
);

const Category = ({ title, items }) => (
  <div className="grid grid-cols-[80px_1fr] md:grid-cols-[110px_1fr] gap-4 md:gap-6 mb-8">
    <div className="vino-mono text-[11px] md:text-[13px] tracking-[0.3em] text-[#f2e8cf] pt-2">
      {title}
    </div>
    <div>
      {items.map((it, i) => (
        <WineRow key={i} name={it.name} price={it.price} />
      ))}
    </div>
  </div>
);

const WineList = React.forwardRef((props, ref) => {
  return (
    <section ref={ref} id="wine" className="relative bg-[#4a4d2c] py-24 md:py-32 px-6">
      <div className="max-w-[1400px] mx-auto">
        <h2 className="vino-display text-[#f2e8cf] text-6xl md:text-8xl text-center tracking-[0.08em] mb-4">
          WINE LIST
        </h2>
        <div className="h-px w-full bg-[#f2e8cf]/30 mb-16 md:mb-20" />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-16 lg:gap-x-24">
          <div>
            <Category title="FIZZ" items={wineData.fizz} />
            <Category title="WHITE" items={wineData.white} />
          </div>
          <div>
            <Category title="ORANGE" items={wineData.orange} />
            <Category title="ROSE" items={wineData.rose} />
            <Category title="RED" items={wineData.red} />
          </div>
        </div>

        <div className="h-px w-full bg-[#f2e8cf]/30 mt-16 md:mt-20" />
        <div className="flex justify-center mt-8">
          <div className="h-10 w-px bg-[#f2e8cf]/50" />
        </div>
      </div>
    </section>
  );
});

export default WineList;
