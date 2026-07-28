'use client';

import { motion } from 'framer-motion';
import { TestimonialCard, type Testimonial } from '@/components/testimonials/testimonial-card';
import { SectionHeading } from '@/components/ui/section-heading';
import { staggerContainer } from '@/lib/motion';

const TESTIMONIALS: Testimonial[] = [
  {
    name: 'Layla Hassan',
    role: 'Content Creator',
    quote:
      'I used to skim comments manually for hours. Now I get a clear sentiment breakdown in minutes, and it actually changed how I plan my videos.',
    initials: 'LH',
  },
  {
    name: 'Marcus Chen',
    role: 'Marketing Analyst',
    quote:
      'The keyword extraction alone justified the switch. We spot recurring complaints across campaigns before they show up in support tickets.',
    initials: 'MC',
  },
  {
    name: 'Sara Ahmadi',
    role: 'Data Scientist',
    quote:
      'Dual-model support for Arabic and English is rare to find done well. The confidence scores are consistent with what I get from my own models.',
    initials: 'SA',
  },
  {
    name: 'Daniel Okafor',
    role: 'Community Manager',
    quote:
      'Spam detection cut our manual moderation queue by more than half. The PDF reports are clean enough to hand straight to leadership.',
    initials: 'DO',
  },
  {
    name: 'Priya Nair',
    role: 'Content Creator',
    quote:
      'Sarcasm detection is the feature I didn\'t know I needed. It catches tone my old sentiment tool completely missed.',
    initials: 'PN',
  },
  {
    name: 'Omar Farouk',
    role: 'Marketing Analyst',
    quote:
      'CSV export means our whole team can work with the data in the tools we already use. No lock-in, no extra training.',
    initials: 'OF',
  },
];

export function Testimonials() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="What people are saying"
          title="Loved by creators and analysts"
        />

        <motion.div
          variants={staggerContainer(0.08)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          {TESTIMONIALS.map((testimonial) => (
            <TestimonialCard key={testimonial.name} testimonial={testimonial} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}