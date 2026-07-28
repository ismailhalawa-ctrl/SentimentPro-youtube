const BARS = [40, 65, 45, 80, 60, 90, 70];

export function MiniChart() {
  const max = Math.max(...BARS);
  return (
    <svg viewBox="0 0 140 48" className="h-12 w-full" aria-hidden="true">
      {BARS.map((value, i) => {
        const height = (value / max) * 40;
        const barWidth = 140 / BARS.length - 4;
        const x = i * (140 / BARS.length) + 2;
        const y = 44 - height;
        const isLast = i === BARS.length - 1;
        return (
          <rect
            key={i}
            x={x}
            y={y}
            width={barWidth}
            height={height}
            rx={2}
            className={isLast ? 'fill-brand-500' : 'fill-brand-500/30'}
          />
        );
      })}
    </svg>
  );
}