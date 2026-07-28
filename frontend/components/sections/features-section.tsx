'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import {
  Smile,
  ShieldAlert,
  Drama,
  Sparkles,
  Tags,
  FileText,
  Sheet,
  LayoutDashboard,
  Languages,
  ArrowRight,
} from 'lucide-react';
import { SectionHeading } from '@/components/ui/section-heading';
import { Button } from '@/components/ui/button';
import { staggerContainer } from '@/lib/motion';
import { FeatureCard, type Feature } from './feature-card';

const FEATURES: Feature[] = [
  {
    title: 'Sentiment Analysis',
    description: 'Detect positive, negative, and neutral emotions in every comment.',
    icon: Smile,
  },
  {
    title: 'Spam Detection',
    description: 'Identify spam and unwanted comments before they skew your results.',
    icon: ShieldAlert,
  },
  {
    title: 'Sarcasm Detection',
    description: 'Catch sarcastic and complex language patterns other tools miss.',
    icon: Drama,
  },
  {
    title: 'AI Insights',
    description: 'Generate meaningful summaries and audience insights automatically.',
    icon: Sparkles,
  },
  {
    title: 'Keyword Extraction',
    description: 'Extract the topics and keywords your audience talks about most.',
    icon: Tags,
  },
  {
    title: 'PDF Reports',
    description: 'Generate professional, shareable analysis reports in one click.',
    icon: FileText,
  },
  {
    title: 'CSV Export',
    description: 'Export raw analyzed data for your own pipelines and spreadsheets.',
    icon: Sheet,
  },
  {
    title: 'Interactive Dashboard',
    description: 'Visualize results with charts and analytics that update live.',
    icon: LayoutDashboard,
  },
  {
    title: 'Multilingual Support',
    description: 'Analyze comments across multiple languages, including Arabic.',
    icon: Languages,
  },
];

export function FeaturesSection() {
  return (
    <section id="features" className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="Everything you need"
          title="Built for Creators and Analysts"
          description="Nine AI-powered capabilities that turn raw comments into decisions."
        />

        <motion.div
          variants={staggerContainer(0.06)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          {FEATURES.map((feature) => (
            <FeatureCard key={feature.title} feature={feature} />
          ))}
        </motion.div>

        {}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-16 flex justify-center"
        >
          <Link href="/register" passHref>
            <Button variant="primary" size="lg" className="group">
              Get Started Now
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
}