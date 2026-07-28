export function CodeBlock({ label, code }: { label: string; code: string }) {
  return (
    <div className="overflow-hidden rounded-md border border-border-subtle bg-background-base">
      <p className="border-b border-border-subtle px-4 py-2 text-xs font-medium uppercase tracking-wide text-text-muted">
        {label}
      </p>
      <pre className="overflow-x-auto p-4 text-xs leading-relaxed text-text-secondary">
        <code className="font-mono">{code}</code>
      </pre>
    </div>
  );
}
