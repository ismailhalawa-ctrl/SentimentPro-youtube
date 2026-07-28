'use client';

import { motion } from 'framer-motion';
import { PricingCard, type PricingTier } from '@/components/pricing/pricing-card';
import { staggerContainer } from '@/lib/motion';

const TIERS: PricingTier[] = [
  {
    name: 'Free',
    price: '$0',
    priceSuffix: '/ forever',
    tagline: 'Get a feel for AI-powered comment analysis on smaller videos.',
    features: [
      'Up to 100 comments per analysis',
      'Fast Mode sentiment analysis (local models)',
      'Basic dashboard — sentiment & spam breakdown',
      '3 analyses per month',
      'CSV export',
      'Community support',
    ],
    ctaLabel: 'Get Started Free',
    ctaHref: '/register',
  },
  {
    name: 'Creator / Pro',
    price: '$29',
    priceSuffix: '/ month',
    tagline: 'Deep, reliable insights for creators and analysts who publish regularly.',
    features: [
      'Up to 10,000 comments per analysis',
      'Fast, Hybrid & Smart AI modes',
      'Deep insights — summaries, topics, complaints, suggestions, FAQs',
      'Audience Intelligence scoring & personas',
      'AI RAG chatbot comment assistant',
      'PDF, CSV & Excel export',
      'Unlimited analyses',
      'Priority email support',
    ],
    ctaLabel: 'Start with Pro',
    ctaHref: '/register',
    highlighted: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    tagline: 'Custom volume, dedicated infrastructure, and white-glove support at scale.',
    features: [
      'Custom volumes — 80,000+ comments per analysis',
      'Dedicated RAG chatbot support & tuning',
      'Priority processing queue',
      'Dedicated infrastructure & onboarding',
      'Single sign-on (SSO) available',
      'Custom SLA & dedicated account manager',
    ],
    ctaLabel: 'Contact Sales',
    ctaHref: '/contact',
  },
];

export function PricingTiersSection() {
  return (
    <section className="relative pb-20 sm:pb-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={staggerContainer(0.08)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 items-stretch gap-6 lg:grid-cols-3"
        >
          {TIERS.map((tier) => (
            <PricingCard key={tier.name} tier={tier} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
