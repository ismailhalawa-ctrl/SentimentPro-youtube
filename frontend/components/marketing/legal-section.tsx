export interface LegalSectionData {
  heading: string;
  body: React.ReactNode;
}

export function LegalSection({ index, heading, body }: LegalSectionData & { index: number }) {
  return (
    <section className="border-t border-border-subtle py-8 first:border-t-0 first:pt-0">
      <h2 className="flex items-baseline gap-3 text-xl font-semibold text-text-primary">
        <span className="text-brand-400">{String(index + 1).padStart(2, '0')}</span>
        {heading}
      </h2>
      <div className="mt-3 flex flex-col gap-3 text-sm leading-relaxed text-text-secondary [&_a]:text-brand-400 [&_a:hover]:text-brand-500 [&_li]:ml-5 [&_li]:list-disc [&_strong]:text-text-primary">
        {body}
      </div>
    </section>
  );
}
