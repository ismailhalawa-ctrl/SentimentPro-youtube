const STATS = [
  { label: 'Positive', value: '62%', colorClass: 'text-sentiment-positive', dotClass: 'bg-sentiment-positive' },
  { label: 'Neutral', value: '24%', colorClass: 'text-sentiment-neutral', dotClass: 'bg-sentiment-neutral' },
  { label: 'Negative', value: '14%', colorClass: 'text-sentiment-negative', dotClass: 'bg-sentiment-negative' },
];

export function SentimentStatsRow() {
  return (
    <div className="grid grid-cols-3 gap-3">
      {STATS.map((stat) => (
        <div
          key={stat.label}
          className="rounded-md border border-border-subtle bg-background-surface/60 p-3"
        >
          <div className="flex items-center gap-1.5">
            <span className={`h-1.5 w-1.5 rounded-full ${stat.dotClass}`} />
            <span className="text-xs text-text-muted">{stat.label}</span>
          </div>
          <p className={`mt-1 text-lg font-semibold ${stat.colorClass}`}>{stat.value}</p>
        </div>
      ))}
    </div>
  );
}