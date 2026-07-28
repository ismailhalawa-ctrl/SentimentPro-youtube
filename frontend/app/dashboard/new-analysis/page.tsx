'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { YouTubeUrlInput, isValidYouTubeUrl } from '@/components/analysis/youtube-url-input';
import { VideoPreview } from '@/components/analysis/video-preview';
import {
  AnalysisOptions,
  DEFAULT_ANALYSIS_OPTIONS,
  type AnalysisOptionsState,
} from '@/components/analysis/analysis-options';
import { AnalysisSummary } from '@/components/analysis/analysis-summary';
import { AnalysisProgress } from '@/components/analysis/analysis-progress';
import { StartAnalysisButton } from '@/components/analysis/start-analysis-button';
import { AnalysisResultsBlock } from '@/components/analysis/analysis-results-block';
import { Button } from '@/components/ui/button';
import { useAnalysisJob } from '@/features/analysis/hooks/use-analysis-job';
import { loadDashboardPreferences } from '@/features/settings/use-dashboard-preferences';
import { useLanguage } from '@/lib/i18n/language-provider';
import type { CreateAnalysisJobPayload } from '@/features/analysis/types';

const ALL_COMMENTS_SENTINEL = 1_000_000;

function toJobPayload(url: string, options: AnalysisOptionsState): CreateAnalysisJobPayload {
  return {
    url,
    max_comments: options.analyzeAllComments ? ALL_COMMENTS_SENTINEL : options.maxComments,
    language: options.language,
    mode: options.sentimentEngine,
    order: options.sortOrder,
    keyword_extraction: options.keywordExtraction,
    generate_report: options.generateReport,
  };
}

export default function NewAnalysisPage() {
  const { t } = useLanguage();
  const [url, setUrl] = useState('');
  const [compareUrl, setCompareUrl] = useState('');
  const [options, setOptions] = useState<AnalysisOptionsState>(DEFAULT_ANALYSIS_OPTIONS);

  useEffect(() => {
    const prefs = loadDashboardPreferences();
    setOptions((current) => ({
      ...current,
      language: prefs.defaultLanguage,
      maxComments: prefs.defaultMaxComments,
    }));
  }, []);

  const primary = useAnalysisJob();
  const compare = useAnalysisJob();

  const isPrimaryUrlValid = isValidYouTubeUrl(url);
  const isCompareUrlValid = isValidYouTubeUrl(compareUrl);
  const isCompareMode = options.mode === 'compare';

  const isUrlValid = isCompareMode ? isPrimaryUrlValid && isCompareUrlValid : isPrimaryUrlValid;
  const isRunning = primary.isRunning || (isCompareMode && compare.isRunning);

  async function handleStart() {
    await primary.start(toJobPayload(url, options));
    if (isCompareMode) {
      await compare.start(toJobPayload(compareUrl, options));
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-text-primary">{t('newAnalysis.title')}</h1>
        <p className="mt-1 text-sm text-text-secondary">{t('newAnalysis.subtitle')}</p>
      </div>

      <YouTubeUrlInput
        id="youtube-url-primary"
        label={isCompareMode ? t('newAnalysis.urlLabelA') : t('newAnalysis.urlLabel')}
        value={url}
        onChange={setUrl}
      />

      <AnimatePresence>
        {isCompareMode && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <YouTubeUrlInput
              id="youtube-url-compare"
              label={t('newAnalysis.urlLabelB')}
              value={compareUrl}
              onChange={setCompareUrl}
            />
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {(isPrimaryUrlValid || (isCompareMode && isCompareUrlValid)) && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <VideoPreview url={url} compareUrl={compareUrl} mode={options.mode} />
          </motion.div>
        )}
      </AnimatePresence>

      <AnalysisOptions options={options} onChange={setOptions} />

      <AnalysisSummary options={options} />

      <div>
        <StartAnalysisButton isValid={isUrlValid && !isRunning} isRunning={isRunning} onClick={handleStart} />
      </div>

      <AnimatePresence>
        {(primary.error || compare.error) && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="rounded-md border border-feedback-danger/20 bg-feedback-danger/10 p-3 text-sm text-feedback-danger"
          >
            {t('newAnalysis.errorPrefix')} {primary.error || compare.error}
          </motion.p>
        )}
      </AnimatePresence>

      {}
      <AnimatePresence>
        {primary.job && primary.job.status !== 'completed' && !primary.error && (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
            <AnalysisProgress
              job={primary.job}
              label={isCompareMode ? t('newAnalysis.videoA') : t('newAnalysis.progressLabel')}
              onCancel={primary.cancel}
              isCancelling={primary.isCancelling}
            />
          </motion.div>
        )}
      </AnimatePresence>
      {isCompareMode && compare.job && compare.job.status !== 'completed' && !compare.error && (
        <AnalysisProgress
          job={compare.job}
          label={t('newAnalysis.videoB')}
          onCancel={compare.cancel}
          isCancelling={compare.isCancelling}
        />
      )}

      <AnimatePresence>
        {primary.job?.status === 'completed' && primary.job.sentiment_summary && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col gap-6"
          >
            <div className="flex items-center justify-between rounded-md border border-sentiment-positive/20 bg-sentiment-positive/10 p-4 text-sm text-sentiment-positive">
              <span>
                ✨{' '}
                {t('newAnalysis.complete.banner', {
                  title: primary.job.video_title || t('newAnalysis.videoFallback'),
                  count:
                    primary.job.sentiment_summary.positive_count +
                    primary.job.sentiment_summary.neutral_count +
                    primary.job.sentiment_summary.negative_count,
                })}
              </span>
              <Link href="/dashboard/history" className="shrink-0">
                <Button variant="ghost" size="sm">
                  {t('newAnalysis.complete.viewHistory')} <ArrowRight className="h-3.5 w-3.5" />
                </Button>
              </Link>
            </div>

            {isCompareMode && <p className="text-sm font-medium text-text-secondary">{t('newAnalysis.videoA')}</p>}
            <AnalysisResultsBlock job={primary.job} />

            {isCompareMode && compare.job?.status === 'completed' && compare.job.sentiment_summary && (
              <>
                <p className="text-sm font-medium text-text-secondary">{t('newAnalysis.videoB')}</p>
                <AnalysisResultsBlock job={compare.job} />
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
