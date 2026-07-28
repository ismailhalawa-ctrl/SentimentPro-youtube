'use client';

import { motion } from 'framer-motion';
import { Link2, Cpu, BarChart3, ShieldCheck } from 'lucide-react';

const STEPS = [
  {
    title: '1. Paste Video Link',
    description: 'Copy any public YouTube video URL and enter it into the analysis field.',
    icon: Link2,
    variant: 'brand',
  },
  {
    title: '2. AI Processing',
    description: 'Our advanced NLP models fetch and classify comments into positive, neutral, or negative.',
    icon: Cpu,
    variant: 'purple',
  },
  {
    title: '3. Interactive Metrics',
    description: 'Explore deep sentiment trends, key phrases, and emotional distribution instantly.',
    icon: BarChart3,
    variant: 'blue',
  },
  {
    title: '4. Export Reports',
    description: 'Download PDF or CSV summaries of your audience feedback for presentations.',
    icon: ShieldCheck,
    variant: 'muted',
  },
];

export function QuickActions() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {STEPS.map((step, idx) => {
        const Icon = step.icon;
        return (
          <motion.div
            key={step.title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: idx * 0.05, ease: 'easeOut' }}
            className="flex h-full flex-col justify-between rounded-xl border border-border-subtle bg-background-surface/20 p-5 backdrop-blur-sm"
          >
            <div className="space-y-4">
              <div className={`flex h-10 w-10 items-center justify-center rounded-lg border ${
                step.variant === 'brand' ? 'border-brand-500/20 bg-brand-500/10 text-brand-400' :
                step.variant === 'purple' ? 'border-purple-500/20 bg-purple-500/10 text-purple-400' :
                step.variant === 'blue' ? 'border-blue-500/20 bg-blue-500/10 text-blue-400' :
                'border-border-subtle bg-background-elevated text-text-secondary'
              }`}>
                <Icon className="h-5 w-5" />
              </div>
              <div className="space-y-1">
                <h3 className="text-sm font-semibold text-text-primary">
                  {step.title}
                </h3>
                <p className="text-xs text-text-muted leading-relaxed">{step.description}</p>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}