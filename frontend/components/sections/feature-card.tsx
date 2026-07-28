'use client';

import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export interface Feature {
  title: string;
  description: string;
  icon: LucideIcon;
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function FeatureCard({ feature }: { feature: Feature }) {
  const Icon = feature.icon;

  return (
    <motion.div variants={cardVariants} transition={{ duration: 0.4, ease: 'easeOut' }}>
      <Card
        variant="glass"
        className="group h-full p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-glow-brand"
      >
        <CardContent className="flex h-full flex-col gap-3 p-0">
          <span className="flex h-10 w-10 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
            <Icon className="h-5 w-5" />
          </span>
          <p className="text-base font-semibold text-text-primary">{feature.title}</p>
          <p className="text-sm text-text-secondary">{feature.description}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}