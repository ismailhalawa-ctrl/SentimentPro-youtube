'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface PricingTier {
  name: string;
  price: string;
  priceSuffix?: string;
  tagline: string;
  features: string[];
  ctaLabel: string;
  ctaHref: string;
  highlighted?: boolean;
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function PricingCard({ tier }: { tier: PricingTier }) {
  return (
    <motion.div variants={cardVariants} transition={{ duration: 0.4, ease: 'easeOut' }} className="h-full">
      <Card
        variant={tier.highlighted ? 'elevated' : 'glass'}
        className={cn(
          'relative flex h-full flex-col p-6 sm:p-8',
          tier.highlighted && 'border-brand-500 shadow-glow-brand'
        )}
      >
        {tier.highlighted && (
          <Badge status="info" className="absolute -top-3 left-1/2 -translate-x-1/2">
            Most Popular
          </Badge>
        )}
        <CardContent className="flex h-full flex-col p-0">
          <p className="text-sm font-semibold text-text-primary">{tier.name}</p>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-4xl font-bold text-text-primary">{tier.price}</span>
            {tier.priceSuffix && <span className="text-sm text-text-muted">{tier.priceSuffix}</span>}
          </div>
          <p className="mt-2 text-sm text-text-secondary">{tier.tagline}</p>

          <ul className="mt-6 flex flex-1 flex-col gap-3">
            {tier.features.map((feature) => (
              <li key={feature} className="flex items-start gap-2.5 text-sm text-text-secondary">
                <Check className="mt-0.5 h-4 w-4 shrink-0 text-feedback-success" />
                {feature}
              </li>
            ))}
          </ul>

          <Link href={tier.ctaHref} passHref className="mt-8 w-full">
            <Button variant={tier.highlighted ? 'primary' : 'secondary'} size="lg" className="w-full">
              {tier.ctaLabel}
            </Button>
          </Link>
        </CardContent>
      </Card>
    </motion.div>
  );
}
