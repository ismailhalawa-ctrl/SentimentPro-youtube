'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Link2,
  SlidersHorizontal,
  LayoutDashboard,
  MessagesSquare,
  Zap,
  Shuffle,
  BrainCircuit,
  Trash2,
  Download,
} from 'lucide-react';
import { SectionHeading } from '@/components/ui/section-heading';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FaqItem, type FaqItemData } from '@/components/faq/faq-item';
import { WorkflowStep, type WorkflowStepData } from '@/components/workflow/workflow-step';
import { staggerContainer, fadeUpItem } from '@/lib/motion';

const GETTING_STARTED_STEPS: WorkflowStepData[] = [
  {
    number: 1,
    title: 'Create your account',
    description: 'Sign up with email, or continue with Google for one-click access.',
    icon: Link2,
  },
  {
    number: 2,
    title: 'Paste a YouTube link',
    description: 'From New Analysis, paste any public YouTube video URL to get started.',
    icon: SlidersHorizontal,
  },
  {
    number: 3,
    title: 'Choose your mode & limits',
    description: 'Pick Fast, Hybrid, or Smart mode and how many comments to pull in.',
    icon: LayoutDashboard,
  },
  {
    number: 4,
    title: 'Ask the AI assistant',
    description: 'Once analysis completes, chat with your data to dig into any question.',
    icon: MessagesSquare,
  },
];

interface ModeInfo {
  name: string;
  bestFor: string;
  description: string;
  icon: typeof Zap;
  accent: string;
}

const MODES: ModeInfo[] = [
  {
    name: 'Fast Mode',
    bestFor: 'Best for: quick checks, no API key required',
    description:
      'Runs entirely on our own locally-hosted transformer models (MARBERT for Arabic, RoBERTa for English). Every comment is classified for sentiment, spam, and sarcasm instantly, with no external API calls and no per-comment cost.',
    icon: Zap,
    accent: 'text-feedback-success',
  },
  {
    name: 'Hybrid Mode',
    bestFor: 'Best for: balancing speed, cost, and accuracy',
    description:
      'Runs Fast Mode across every comment first, then automatically escalates only the uncertain ones — low local-model confidence, sarcasm, mixed-language/Arabizi text, or heavy emoji use — to a large language model for a second opinion.',
    icon: Shuffle,
    accent: 'text-brand-400',
  },
  {
    name: 'Smart Mode',
    bestFor: 'Best for: maximum depth on smaller comment sets',
    description:
      'Sends comments through a large language model (OpenAI or Google Gemini) for the deepest per-comment reasoning, including nuanced sarcasm and dialect understanding — the most thorough option, at LLM API cost.',
    icon: BrainCircuit,
    accent: 'text-feedback-warning',
  },
];

const DOCS_FAQS: FaqItemData[] = [
  {
    question: 'Which mode should I use by default?',
    answer:
      'Start with Fast Mode for a quick, free read on any video. Switch to Hybrid when you want LLM-level accuracy on the comments that actually need it, without paying for every single one. Reach for Smart Mode when you want maximum depth on a smaller, high-stakes comment set.',
  },
  {
    question: 'Do I need my own OpenAI or Gemini API key?',
    answer:
      "No — Hybrid and Smart mode work out of the box on paid plans. If no AI provider is configured, those modes gracefully fall back to Fast Mode's local models rather than failing.",
  },
  {
    question: 'How do I ask the AI assistant a good question?',
    answer:
      'Be specific and natural — "What are people complaining about most?" or "Summarize the sarcastic comments" both work well. The assistant remembers your conversation, so follow-ups like "why?" build on what was just discussed.',
  },
  {
    question: 'Can I export my results?',
    answer:
      'Yes — every completed analysis can be exported as CSV or Excel (full per-comment data) or as a PDF summary report, from the export button on the analysis detail page.',
  },
  {
    question: 'How do I delete an analysis?',
    answer:
      'Open the History page, click the trash icon on any analysis card, and confirm — this permanently removes its comments, insights, and chat history. "Clear All History" removes everything at once.',
  },
];

export function DocsContent() {
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);

  return (
    <>
      <section className="relative pb-20 sm:pb-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <SectionHeading
            eyebrow="Getting started"
            title="From link to insight in four steps"
            description="The fastest path from a YouTube URL to a full sentiment breakdown."
          />
          <motion.div
            variants={staggerContainer(0.1)}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            className="mt-14 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
          >
            {GETTING_STARTED_STEPS.map((step) => (
              <WorkflowStep key={step.number} step={step} />
            ))}
          </motion.div>
        </div>
      </section>

      <section className="relative border-t border-border-subtle py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <SectionHeading
            eyebrow="Analysis modes"
            title="Fast, Hybrid, or Smart — pick your depth"
            description="Every analysis runs in one of three modes, trading off speed, cost, and depth."
          />
          <motion.div
            variants={staggerContainer(0.1)}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-100px' }}
            className="mt-14 grid grid-cols-1 gap-6 lg:grid-cols-3"
          >
            {MODES.map((mode) => {
              const Icon = mode.icon;
              return (
                <motion.div key={mode.name} variants={fadeUpItem} transition={{ duration: 0.4, ease: 'easeOut' }}>
                  <Card variant="glass" className="h-full p-6">
                    <CardContent className="flex h-full flex-col gap-3 p-0">
                      <span className={`flex h-10 w-10 items-center justify-center rounded-md bg-background-elevated ${mode.accent}`}>
                        <Icon className="h-5 w-5" />
                      </span>
                      <p className="text-lg font-semibold text-text-primary">{mode.name}</p>
                      <p className="text-xs font-medium uppercase tracking-wide text-text-muted">{mode.bestFor}</p>
                      <p className="text-sm text-text-secondary">{mode.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      <section className="relative border-t border-border-subtle py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <SectionHeading
            eyebrow="AI comment assistant"
            title="Chat with your comment data"
            description="Every completed analysis includes a RAG-powered assistant grounded in that video's actual comments."
          />
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="mt-10"
          >
            <Card variant="glass" className="p-6 sm:p-8">
              <CardContent className="flex flex-col gap-4 p-0 text-sm text-text-secondary">
                <p>
                  Open the <strong className="text-text-primary">AI Assistant</strong> tab on any
                  completed analysis and ask a question in plain language, in English, Arabic, or
                  Arabizi. The assistant retrieves the most relevant comments for your question via
                  vector search, and answers using only what those comments actually say — never
                  inventing statistics or quotes.
                </p>
                <ul className="flex flex-col gap-2">
                  <li className="flex items-start gap-2.5">
                    <Badge status="info" className="mt-0.5 shrink-0">Grounded</Badge>
                    Every answer is citation-backed against real comments from that analysis.
                  </li>
                  <li className="flex items-start gap-2.5">
                    <Badge status="success" className="mt-0.5 shrink-0">Multi-turn</Badge>
                    The assistant remembers your conversation, so follow-up questions build naturally.
                  </li>
                  <li className="flex items-start gap-2.5">
                    <Badge status="warning" className="mt-0.5 shrink-0">Dialect-aware</Badge>
                    Understands Egyptian, Levantine, and Gulf Arabic dialects as well as sarcasm.
                  </li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </section>

      <section className="relative border-t border-border-subtle py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <SectionHeading
            eyebrow="Managing your results"
            title="Export, revisit, or clean up anytime"
          />
          <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
            <Card variant="glass" className="p-6">
              <CardContent className="flex flex-col gap-3 p-0">
                <span className="flex h-10 w-10 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                  <Download className="h-5 w-5" />
                </span>
                <p className="text-base font-semibold text-text-primary">Export your results</p>
                <p className="text-sm text-text-secondary">
                  Download full per-comment data as CSV or Excel, or a shareable PDF summary report,
                  from the export button on any completed analysis.
                </p>
              </CardContent>
            </Card>
            <Card variant="glass" className="p-6">
              <CardContent className="flex flex-col gap-3 p-0">
                <span className="flex h-10 w-10 items-center justify-center rounded-md bg-feedback-danger/15 text-feedback-danger">
                  <Trash2 className="h-5 w-5" />
                </span>
                <p className="text-base font-semibold text-text-primary">Clean up your history</p>
                <p className="text-sm text-text-secondary">
                  Delete a single analysis, or use &ldquo;Clear All History&rdquo; from the History page
                  to permanently remove everything at once.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <section className="relative border-t border-border-subtle py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <SectionHeading eyebrow="Common questions" title="Documentation FAQ" className="text-center" />
          <div className="mt-12 flex flex-col gap-4">
            {DOCS_FAQS.map((item, index) => (
              <FaqItem
                key={item.question}
                item={item}
                index={index}
                isOpen={openFaqIndex === index}
                onToggle={() => setOpenFaqIndex(openFaqIndex === index ? null : index)}
              />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
