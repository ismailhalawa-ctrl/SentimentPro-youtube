'use client';

import { motion } from 'framer-motion';
import { ArrowRight, PlayCircle } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

export function FinalCta() {
  return (
    <section className="relative overflow-hidden py-20 sm:py-28">
      <div className="bg-radial-glow pointer-events-none absolute inset-0" />

      <motion.div
        animate={{ y: [0, -16, 0], x: [0, 12, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        className="pointer-events-none absolute left-1/4 top-1/4 h-56 w-56 rounded-full bg-brand-500/20 blur-3xl"
      />
      <motion.div
        animate={{ y: [0, 20, 0], x: [0, -14, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        className="pointer-events-none absolute bottom-1/4 right-1/4 h-64 w-64 rounded-full bg-brand-400/15 blur-3xl"
      />

      <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <Card variant="glass" className="p-10 text-center sm:p-14">
            <CardContent className="flex flex-col items-center gap-6 p-0">
              <h2 className="text-3xl font-bold leading-tight text-text-primary sm:text-4xl">
                Turn YouTube Comments Into{' '}
                <span className="bg-gradient-brand bg-clip-text text-transparent">
                  Actionable Insights
                </span>
              </h2>
              <p className="max-w-xl text-lg text-text-secondary">
                Analyze audience feedback with AI-powered NLP models and generate
                clear, exportable insights in minutes.
              </p>
              <div className="flex flex-col gap-3 sm:flex-row">

                {}
                <Link href="/login" passHref className="w-full sm:w-auto">
                  <Button variant="primary" size="lg" className="group w-full">
                    Start Analyzing
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                  </Button>
                </Link>

                {}
                <Link href="/dashboard" passHref className="w-full sm:w-auto">
                  <Button variant="secondary" size="lg" className="w-full">
                    <PlayCircle className="h-4 w-4" />
                    Explore Demo
                  </Button>
                </Link>

              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}