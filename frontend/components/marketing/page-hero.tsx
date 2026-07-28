'use client';

import { motion } from 'framer-motion';

export interface PageHeroProps {
  eyebrow: string;
  title: string;
  description?: string;
}

export function PageHero({ eyebrow, title, description }: PageHeroProps) {
  return (
    <section className="relative overflow-hidden py-20 sm:py-28">
      <div className="bg-radial-glow pointer-events-none absolute inset-0" />
      <div className="relative mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <p className="text-sm font-medium text-brand-400">{eyebrow}</p>
          <h1 className="mt-2 text-4xl font-bold leading-tight text-text-primary sm:text-5xl">
            {title}
          </h1>
          {description && <p className="mt-4 text-lg text-text-secondary">{description}</p>}
        </motion.div>
      </div>
    </section>
  );
}
