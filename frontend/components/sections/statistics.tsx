'use client';

import { motion } from 'framer-motion';
import { MessageSquareText, Target, FileText, Users } from 'lucide-react';
import { StatCard, type StatisticData } from '@/components/statistics/stat-card';
import { SectionHeading } from '@/components/ui/section-heading';
import { staggerContainer } from '@/lib/motion';

const STATISTICS: StatisticData[] = [
  {
    value: 250000,
    suffix: '+',
    title: 'Comments Analyzed',
    description: 'Processed across thousands of videos.',
    icon: MessageSquareText,
  },
  {
    value: 95,
    suffix: '%+',
    title: 'AI Accuracy',
    description: 'Validated against human-labeled datasets.',
    icon: Target,
  },
  {
    value: 50000,
    suffix: '+',
    title: 'Reports Generated',
    description: 'PDF and CSV exports delivered to creators.',
    icon: FileText,
  },
  {
    value: 10000,
    suffix: '+',
    title: 'Active Users',
    description: 'Creators and analysts using the platform.',
    icon: Users,
  },
];

export function Statistics() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="Trusted at scale"
          title="Numbers that speak for themselves"
        />

        <motion.div
          variants={staggerContainer(0.08)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4"
        >
          {STATISTICS.map((stat) => (
            <StatCard key={stat.title} stat={stat} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}