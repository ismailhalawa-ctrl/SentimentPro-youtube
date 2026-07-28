'use client';

import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { AnimatedCounter } from './animated-counter';

export interface StatisticData {
  value: number;
  suffix: string;
  title: string;
  description: string;
  icon: LucideIcon;
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function StatCard({ stat }: { stat: StatisticData }) {
  const Icon = stat.icon;

  return (
    <motion.div variants={cardVariants} transition={{ duration: 0.4, ease: 'easeOut' }}>
      <Card
        variant="glass"
        className="group h-full p-6 text-center transition-all duration-300 hover:-translate-y-1 hover:shadow-glow-brand"
      >
        <CardContent className="flex h-full flex-col items-center gap-2 p-0">
          <span className="flex h-10 w-10 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
            <Icon className="h-5 w-5" />
          </span>
          <p className="mt-2 text-3xl font-bold text-text-primary sm:text-4xl">
            <AnimatedCounter value={stat.value} suffix={stat.suffix} />
          </p>
          <p className="text-base font-semibold text-text-primary">{stat.title}</p>
          <p className="text-sm text-text-secondary">{stat.description}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}