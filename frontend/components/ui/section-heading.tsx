'use client';

import { motion } from 'framer-motion';

export interface SectionHeadingProps {
  eyebrow: string;
  title: string;
  description?: string;
  className?: string;
}

export function SectionHeading({ eyebrow, title, description, className }: SectionHeadingProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={className ?? 'mx-auto max-w-2xl text-center'}
    >
      <p className="text-sm font-medium text-brand-400">{eyebrow}</p>
      <h2 className="mt-2 text-3xl font-semibold text-text-primary sm:text-4xl">{title}</h2>
      {description && <p className="mt-3 text-lg text-text-secondary">{description}</p>}
    </motion.div>
  );
}