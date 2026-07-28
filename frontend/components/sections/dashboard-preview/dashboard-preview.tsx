'use client';

import { motion } from 'framer-motion';
import { SentimentScoreCard } from './sentiment-score-card';
import { SentimentStatsRow } from './sentiment-stats-row';
import { AiInsightCard } from './ai-insight-card';
import { RecentCommentsCard } from './recent-comments-card';

export function DashboardPreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
      className="relative w-full max-w-md"
    >
      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        className="flex flex-col gap-4 rounded-xl border border-border-default bg-background-elevated/40 p-5 shadow-lg backdrop-blur-md"
      >
        <SentimentScoreCard />
        <SentimentStatsRow />
        <AiInsightCard />
        <RecentCommentsCard />
      </motion.div>
    </motion.div>
  );
}