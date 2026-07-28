'use client';

import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export interface WorkflowStepData {
  number: number;
  title: string;
  description: string;
  icon: LucideIcon;
}

const stepVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function WorkflowStep({ step }: { step: WorkflowStepData }) {
  const Icon = step.icon;

  return (
    <motion.div variants={stepVariants} transition={{ duration: 0.4, ease: 'easeOut' }}>
      <Card
        variant="glass"
        className="group h-full p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-glow-brand"
      >
        <CardContent className="flex h-full flex-col gap-3 p-0">
          <div className="flex items-center gap-3">
            <span className="text-2xl font-bold text-brand-500">
              {String(step.number).padStart(2, '0')}
            </span>
            <span className="flex h-9 w-9 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
              <Icon className="h-4 w-4" />
            </span>
          </div>
          <p className="text-base font-semibold text-text-primary">{step.title}</p>
          <p className="text-sm text-text-secondary">{step.description}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}