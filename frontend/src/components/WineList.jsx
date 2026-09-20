import React from 'react';

const WineRow = ({ name, price }) => (
  <div className="flex items-baseline gap-4 py-1.5 group">
    <span className="vino-mono text-[11px] md:text-[12.5px] text-bianco/90 leading-relaxed flex-1 group-hover:text-bianco transition-colors">
      {name}
    </span>
    <span className="vino-mono text-[11px] md:text-[12.5px] text-bianco/80 whitespace-nowrap">
      {price}
    </span>
  </div>
);

const Category = ({ title, items }) => {
  if (!items || items.length === 0) return null;
  return (
    <div className="grid grid-cols-[80px_1fr] md:grid-cols-[110px_1fr] gap-4 md:gap-6 mb-8">
      <div className="vino-mono-medium text-[11px] md:text-[13px] tracking-[0.35em] text-bianco pt-1.5">
        {title}
      </div>
      <div>
        {items.map((it, i) => (
          <WineRow key={i} name={it.name} price={it.price} />
        ))}
      </div>
    </div>
  );
};

const WineList = React.forwardRef(({ menu }, ref) => {
  return (
    <section ref={ref} id="wine" className="relative bg-oliva py-12 md:py-16 px-6">
      <div className="max-w-[1400px] mx-auto">
        <div className="flex items-center gap-3 justify-center mb-6">
          <div className="h-px w-10 bg-bianco/50" />
          <span className="vino-mono-medium text-bianco text-[10px] md:text-xs tracking-[0.4em]">LA CARTA DEI VINI</span>
          <div className="h-px w-10 bg-bianco/50" />
        </div>
        <h2 className="vino-display text-bianco text-5xl md:text-8xl text-center tracking-[0.1em] mb-4">
          WINE LIST
        </h2>
        <div className="h-px w-full bg-bianco/25 mb-16 md:mb-20" />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-16 lg:gap-x-24">
          <div>
            <Category title="FIZZ" items={menu?.fizz} />
            <Category title="WHITE" items={menu?.white} />
          </div>
          <div>
            <Category title="ORANGE" items={menu?.orange} />
            <Category title="ROSE" items={menu?.rose} />
            <Category title="RED" items={menu?.red} />
          </div>
        </div>

        <div className="h-px w-full bg-bianco/25 mt-16 md:mt-20" />
        <div className="flex justify-center mt-6">
          <div className="h-8 w-px bg-bianco/50" />
        </div>
      </div>
    </section>
  );
});

export default WineList;
