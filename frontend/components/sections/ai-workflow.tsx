'use client';

import { motion } from 'framer-motion';
import { Link2, Download, Cpu, Sparkles, FileOutput } from 'lucide-react';
import { WorkflowStep, type WorkflowStepData } from '@/components/workflow/workflow-step';
import { SectionHeading } from '@/components/ui/section-heading';
import { staggerContainer } from '@/lib/motion';

const STEPS: WorkflowStepData[] = [
  {
    number: 1,
    title: 'Paste YouTube URL',
    description: 'User provides a YouTube video link.',
    icon: Link2,
  },
  {
    number: 2,
    title: 'Collect Comments',
    description: 'System retrieves comments using the YouTube Data API.',
    icon: Download,
  },
  {
    number: 3,
    title: 'AI Processing',
    description: 'Transformer models analyze sentiment, spam, sarcasm, and patterns.',
    icon: Cpu,
  },
  {
    number: 4,
    title: 'Generate Insights',
    description: 'AI creates summaries, trends, and audience insights.',
    icon: Sparkles,
  },
  {
    number: 5,
    title: 'Export Reports',
    description: 'Users download PDF and CSV reports.',
    icon: FileOutput,
  },
];

export function AiWorkflow() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="How it works"
          title="From link to insight in five steps"
          description="A straightforward pipeline from raw comments to actionable reports."
        />

        <div className="relative mt-16">
          {}
          <div
            className="absolute left-1/2 top-0 hidden h-full w-px bg-gradient-to-b from-transparent via-border-default to-transparent lg:top-1/2 lg:block lg:h-px lg:w-full lg:bg-gradient-to-r"
            aria-hidden="true"
          />

          <motion.div
            variants={staggerContainer(0.1)}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            className="relative grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5"
          >
            {STEPS.map((step) => (
              <WorkflowStep key={step.number} step={step} />
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}