import React, { useMemo } from 'react';

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
      <div className="vino-mono-medium text-[11px] md:text-[13px] tracking-[0.35em] text-bianco pt-1.5 uppercase">
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

// Split categories into two balanced columns based on cumulative row count
const splitCategories = (categories) => {
  const list = (categories || []).filter((c) => c && c.items && c.items.length > 0);
  const total = list.reduce((n, c) => n + (c.items?.length || 0) + 1, 0); // +1 for header "weight"
  const target = total / 2;

  const left = [];
  const right = [];
  let running = 0;
  for (const cat of list) {
    const weight = (cat.items?.length || 0) + 1;
    if (running + weight / 2 <= target || left.length === 0) {
      left.push(cat);
      running += weight;
    } else {
      right.push(cat);
    }
  }
  // If one side is empty (only one category), move it to the left
  if (right.length === 0 && left.length > 1) {
    right.push(left.pop());
  }
  return [left, right];
};

const WineList = React.forwardRef(({ menu }, ref) => {
  const categories = menu?.categories || [];
  const [leftCol, rightCol] = useMemo(() => splitCategories(categories), [categories]);

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

        {categories.length === 0 ? (
          <div className="text-center vino-mono text-bianco/60 text-[12px]">
            No wines on the list yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-16 lg:gap-x-24">
            <div>
              {leftCol.map((c, i) => (
                <Category key={c.name + i} title={c.name} items={c.items} />
              ))}
            </div>
            <div>
              {rightCol.map((c, i) => (
                <Category key={c.name + i} title={c.name} items={c.items} />
              ))}
            </div>
          </div>
        )}

        <div className="h-px w-full bg-bianco/25 mt-16 md:mt-20" />
        <div className="flex justify-center mt-6">
          <div className="h-8 w-px bg-bianco/50" />
        </div>
      </div>
    </section>
  );
});

export default WineList;
