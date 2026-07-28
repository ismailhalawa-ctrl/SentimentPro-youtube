'use client';

import * as React from 'react';
import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface Technology {
  name: string;
  description: string;
  icon: LucideIcon;
  accentColor: string;
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function TechCard({ tech }: { tech: Technology }) {
  const Icon = tech.icon;

  return (
    <motion.div variants={cardVariants} transition={{ duration: 0.4, ease: 'easeOut' }}>
      <Card
        variant="glass"
        className="group h-full p-5 transition-all duration-300 hover:-translate-y-1"
        style={{ '--tech-glow': `${tech.accentColor}40` } as React.CSSProperties}
      >
        <CardContent
          className={cn(
            'flex h-full flex-col gap-3 p-0 rounded-lg',
            'group-hover:shadow-[0_0_24px_var(--tech-glow)]'
          )}
        >
          <span
            className="flex h-10 w-10 items-center justify-center rounded-md border border-border-default"
            style={{ color: tech.accentColor }}
          >
            <Icon className="h-5 w-5" />
          </span>
          <p className="text-base font-semibold text-text-primary">{tech.name}</p>
          <p className="text-sm text-text-secondary">{tech.description}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}