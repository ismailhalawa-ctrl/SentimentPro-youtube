'use client';

import { motion } from 'framer-motion';
import { BarChart3, MessageSquareText, FileText, Smile, type LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { AnimatedCounter } from '@/components/statistics/animated-counter';
import { staggerContainer, fadeUpItem } from '@/lib/motion';
import { useAnalysisHistory } from '@/features/analysis/hooks/use-analysis-history';
import { aggregateSentimentSummaries, getSentimentTotal } from '@/features/analysis/sentiment-utils';

interface UsageStat {
  label: string;
  value: number;
  suffix: string;
  icon: LucideIcon;
  accentClass: string;
}

export function StatisticsOverview() {
  const { jobs } = useAnalysisHistory();
  const completedJobs = jobs.filter((j) => j.status === 'completed' && j.sentiment_summary);

  const aggregate =
    completedJobs.length > 0
      ? aggregateSentimentSummaries(completedJobs.map((j) => j.sentiment_summary!))
      : null;
  const totalComments = aggregate ? getSentimentTotal(aggregate) : 0;
  const positivePct =
    aggregate && totalComments > 0 ? Math.round((aggregate.positive_count / totalComments) * 100) : 0;

  const usageStats: UsageStat[] = [
    {
      label: 'Total Analyses',
      value: completedJobs.length,
      suffix: '',
      icon: BarChart3,
      accentClass: 'text-brand-400',
    },
    {
      label: 'Comments Analyzed',
      value: totalComments,
      suffix: '',
      icon: MessageSquareText,
      accentClass: 'text-brand-400',
    },
    {
      label: 'Reports Generated',
      value: completedJobs.length,
      suffix: '',
      icon: FileText,
      accentClass: 'text-brand-400',
    },
    {
      label: 'Overall Positive Sentiment',
      value: positivePct,
      suffix: '%',
      icon: Smile,
      accentClass: 'text-sentiment-positive',
    },
  ];

  return (
    <motion.div
      variants={staggerContainer(0.06)}
      initial="hidden"
      animate="visible"
      className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4"
    >
      {usageStats.map((stat) => {
        const Icon = stat.icon;
        return (
          <motion.div key={stat.label} variants={fadeUpItem} transition={{ duration: 0.4 }}>
            <Card variant="glass" className="p-4">
              <CardContent className="flex items-center gap-3 p-0">
                <span
                  className={`flex h-9 w-9 items-center justify-center rounded-md bg-background-surface ${stat.accentClass}`}
                >
                  <Icon className="h-4 w-4" />
                </span>
                <div>
                  <p className="text-xs text-text-muted">{stat.label}</p>
                  <p className="text-xl font-semibold text-text-primary">
                    <AnimatedCounter value={stat.value} suffix={stat.suffix} duration={1} />
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
      })}
    </motion.div>
  );
}
