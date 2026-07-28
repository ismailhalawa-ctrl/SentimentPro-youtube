'use client';

import { motion } from 'framer-motion';
import { Cpu, Shuffle, Database, Languages } from 'lucide-react';
import { SectionHeading } from '@/components/ui/section-heading';
import { Card, CardContent } from '@/components/ui/card';
import { staggerContainer, fadeUpItem } from '@/lib/motion';

const PILLARS = [
  {
    title: 'Locally-hosted transformer models',
    description:
      'Fast Mode runs on specialized models we host ourselves — MARBERT for Arabic, RoBERTa for English — trained specifically for short, informal social text like YouTube comments.',
    icon: Cpu,
  },
  {
    title: 'Hybrid LLM escalation',
    description:
      'Rather than sending every comment to an expensive LLM, Hybrid Mode escalates only the ones that actually need a second opinion — uncertain, sarcastic, or mixed-language comments.',
    icon: Shuffle,
  },
  {
    title: 'Vector search & a grounded RAG assistant',
    description:
      'Every analyzed comment set is embedded into a searchable vector index, powering an AI assistant that answers your questions using only what your audience actually said.',
    icon: Database,
  },
  {
    title: 'Built for Arabic and English audiences',
    description:
      'Dialect-aware from the ground up — Levantine, Egyptian, and Gulf Arabic, Arabizi, and mixed-language comments are understood natively, not bolted on.',
    icon: Languages,
  },
];

export function AboutContent() {
  return (
    <>
      <section className="pb-20 sm:pb-24">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="flex flex-col gap-4 text-center text-text-secondary"
          >
            <p>
              SentimentPRO is a deep audience-intelligence platform for YouTube creators, marketing
              teams, and researchers. We turn a wall of comments into a clear picture of what your
              audience actually feels — powered by a combination of specialized local models and
              large language models, chosen deliberately for each job rather than defaulting to
              &ldquo;send everything to an LLM.&rdquo;
            </p>
            <p>
              Our goal is simple: give you insight you can trust, at a speed and cost that scales
              from a 50-comment upload to an 80,000-comment viral video, without asking you to
              choose between accuracy and affordability.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="border-t border-border-subtle py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <SectionHeading
            eyebrow="What powers it"
            title="A deliberately hybrid AI architecture"
            description="Every design choice trades off speed, cost, and depth on purpose — never one-size-fits-all."
          />
          <motion.div
            variants={staggerContainer(0.08)}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2"
          >
            {PILLARS.map((pillar) => {
              const Icon = pillar.icon;
              return (
                <motion.div key={pillar.title} variants={fadeUpItem} transition={{ duration: 0.4, ease: 'easeOut' }}>
                  <Card variant="glass" className="h-full p-6">
                    <CardContent className="flex h-full flex-col gap-3 p-0">
                      <span className="flex h-10 w-10 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                        <Icon className="h-5 w-5" />
                      </span>
                      <p className="text-base font-semibold text-text-primary">{pillar.title}</p>
                      <p className="text-sm text-text-secondary">{pillar.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>
    </>
  );
}
