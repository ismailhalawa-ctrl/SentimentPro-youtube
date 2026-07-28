'use client';

import { motion } from 'framer-motion';
import { Quote } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export interface Testimonial {
  name: string;
  role: string;
  quote: string;
  initials: string;
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
  return (
    <motion.div variants={cardVariants} transition={{ duration: 0.4, ease: 'easeOut' }}>
      <Card
        variant="glass"
        className="group h-full p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-glow-brand"
      >
        <CardContent className="flex h-full flex-col gap-4 p-0">
          <Quote className="h-5 w-5 text-brand-400" />
          <p className="flex-1 text-sm text-text-secondary">{testimonial.quote}</p>
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand-500/15 text-sm font-semibold text-brand-400">
              {testimonial.initials}
            </span>
            <div>
              <p className="text-sm font-medium text-text-primary">{testimonial.name}</p>
              <p className="text-xs text-text-muted">{testimonial.role}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}