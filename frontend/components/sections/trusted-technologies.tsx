'use client';

import { motion } from 'framer-motion';
import { FileCode2, Zap, BrainCircuit, PlayCircle, Database, Code2 } from 'lucide-react';
import { SectionHeading } from '@/components/ui/section-heading';
import { staggerContainer } from '@/lib/motion';
import { TechCard, type Technology } from './tech-card';

const TECHNOLOGIES: Technology[] = [
  {
    name: 'Python',
    description: 'Core language powering the NLP pipeline and data processing.',
    icon: FileCode2,
    accentColor: '#3776AB',
  },
  {
    name: 'FastAPI',
    description: 'High-performance API layer serving sentiment predictions.',
    icon: Zap,
    accentColor: '#059669',
  },
  {
    name: 'Hugging Face Transformers',
    description: 'MARBERT and RoBERTa models for Arabic and English sentiment.',
    icon: BrainCircuit,
    accentColor: '#818CF8',
  },
  {
    name: 'YouTube Data API',
    description: 'Fetches comment threads directly from any public video.',
    icon: PlayCircle,
    accentColor: '#EF4444',
  },
  {
    name: 'PostgreSQL',
    description: 'Reliable storage for analyzed comments and historical trends.',
    icon: Database,
    accentColor: '#3B82F6',
  },
  {
    name: 'React / Next.js',
    description: 'Fast, responsive dashboard for exploring your results.',
    icon: Code2,
    accentColor: '#A1A1AA',
  },
];

export function TrustedTechnologies() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="Built on proven technology"
          title="Trusted Technologies"
          description="A modern stack chosen for accuracy, speed, and reliability at scale."
        />

        <motion.div
          variants={staggerContainer(0.08)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          {TECHNOLOGIES.map((tech) => (
            <TechCard key={tech.name} tech={tech} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}