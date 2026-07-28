'use client';

import dynamic from 'next/dynamic';
import { motion } from 'framer-motion';
import { MessagesSquare, Smile, Frown, ShieldAlert } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { SectionHeading } from '@/components/ui/section-heading';
import { staggerContainer, fadeUpItem } from '@/lib/motion';
import { StatCard, type Stat } from '@/components/dashboard-preview/stat-card';
import { CommentTable } from '@/components/dashboard-preview/comment-table';
import { InsightCard } from '@/components/dashboard-preview/insight-card';
import { KeywordList } from '@/components/dashboard-preview/keyword-list';

const SentimentChart = dynamic(
  () => import('@/components/dashboard-preview/sentiment-chart').then((mod) => mod.SentimentChart),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-72 animate-pulse items-center justify-center rounded-lg border border-border-subtle bg-background-surface/60">
        <span className="text-sm text-text-muted">Loading chart…</span>
      </div>
    ),
  }
);

const STATS: Stat[] = [
  { label: 'Comments Analyzed', value: '12,480', icon: MessagesSquare, accentClass: 'text-brand-400' },
  { label: 'Positive Sentiment', value: '62%', icon: Smile, accentClass: 'text-sentiment-positive' },
  { label: 'Negative Sentiment', value: '14%', icon: Frown, accentClass: 'text-sentiment-negative' },
  { label: 'Spam Detected', value: '318', icon: ShieldAlert, accentClass: 'text-feedback-warning' },
];

export function DashboardPreviewSection() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          eyebrow="See it in action"
          title="From comments to decisions"
          description="A live look at how your analysis results will appear."
        />

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.1 }}
          className="mt-14"
        >
          <Card variant="elevated" className="p-6 sm:p-8">
            <CardContent className="flex flex-col gap-6 p-0">
              <motion.div
                variants={staggerContainer(0.08)}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: '-100px' }}
                className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4"
              >
                {STATS.map((stat) => (
                  <motion.div key={stat.label} variants={fadeUpItem} transition={{ duration: 0.4 }}>
                    <StatCard stat={stat} />
                  </motion.div>
                ))}
              </motion.div>

              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <SentimentChart />
                <CommentTable />
              </div>

              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <InsightCard />
                <KeywordList />
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}