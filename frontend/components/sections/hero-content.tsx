'use client';

import { motion } from 'framer-motion';
import { ArrowRight, PlayCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export function HeroContent() {
  return (
    <div className="flex max-w-xl flex-col gap-6">
      <motion.h1
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="text-4xl font-bold leading-tight text-text-primary sm:text-5xl"
      >
        Understand your audience with{' '}
        <span className="bg-gradient-brand bg-clip-text text-transparent">
          AI Sentiment Analysis
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1, ease: 'easeOut' }}
        className="text-lg text-text-secondary"
      >
        Analyze thousands of YouTube comments in seconds. Dual-model NLP
        detects sentiment in Arabic and English, so you know exactly how
        viewers feel about every video.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2, ease: 'easeOut' }}
        className="flex flex-col gap-3 sm:flex-row"
      >
        {}
        <Link href="/login" passHref className="w-full sm:w-auto">
          <Button variant="primary" size="lg" className="group w-full">
            Analyze Comments
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </Button>
        </Link>

        {}
        <Link href="/dashboard" passHref className="w-full sm:w-auto">
          <Button variant="secondary" size="lg" className="w-full">
            <PlayCircle className="h-4 w-4" />
            View Demo
          </Button>
        </Link>
      </motion.div>
    </div>
  );
}