'use client';

import React, { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/forms/checkbox';
import { useLanguage } from '@/lib/i18n/language-provider';

export type Language = 'auto' | 'ar' | 'en';
export type AnalysisMode = 'single' | 'compare';
export type CommentSortOrder = 'relevance' | 'time';
export type SentimentEngine = 'fast' | 'hybrid' | 'smart';

export interface AnalysisOptionsState {
  mode: AnalysisMode;
  maxComments: number;
  analyzeAllComments: boolean;
  sortOrder: CommentSortOrder;
  includeReplies: boolean;
  language: Language;
  sentimentEngine: SentimentEngine;
  keywordExtraction: boolean;
  generateReport: boolean;
}

export const DEFAULT_ANALYSIS_OPTIONS: AnalysisOptionsState = {
  mode: 'single',
  maxComments: 500,
  analyzeAllComments: false,
  sortOrder: 'relevance',
  includeReplies: false,
  language: 'auto',
  sentimentEngine: 'fast',
  keywordExtraction: true,
  generateReport: false,
};

const SENTIMENT_ENGINE_OPTIONS: { value: SentimentEngine; labelKey: string; descKey: string }[] = [
  { value: 'fast', labelKey: 'newAnalysis.sentimentEngine.fast', descKey: 'newAnalysis.sentimentEngine.fastDesc' },
  {
    value: 'hybrid',
    labelKey: 'newAnalysis.sentimentEngine.hybrid',
    descKey: 'newAnalysis.sentimentEngine.hybridDesc',
  },
  {
    value: 'smart',
    labelKey: 'newAnalysis.sentimentEngine.smart',
    descKey: 'newAnalysis.sentimentEngine.smartDesc',
  },
];

interface AnalysisOptionsProps {
  options: AnalysisOptionsState;
  onChange: (options: AnalysisOptionsState) => void;
}

const TOGGLE_FIELDS: { key: keyof AnalysisOptionsState; labelKey: string }[] = [
  { key: 'keywordExtraction', labelKey: 'newAnalysis.nlpFeatures.keywordExtraction' },
  { key: 'generateReport', labelKey: 'newAnalysis.nlpFeatures.generateReport' },
];

const MAX_COMMENTS_MIN = 50;
const MAX_COMMENTS_MAX = 1_000_000;

export function AnalysisOptions({ options, onChange }: AnalysisOptionsProps) {
  const { t } = useLanguage();

  function update<K extends keyof AnalysisOptionsState>(key: K, value: AnalysisOptionsState[K]) {
    onChange({ ...options, [key]: value });
  }

  const [maxCommentsInput, setMaxCommentsInput] = useState(String(options.maxComments));

  useEffect(() => {
    setMaxCommentsInput(String(options.maxComments));
  }, [options.maxComments]);

  function handleMaxCommentsChange(e: React.ChangeEvent<HTMLInputElement>) {
    const raw = e.target.value;
    setMaxCommentsInput(raw);
    if (raw === '') return;
    const parsed = Number(raw);
    if (!Number.isNaN(parsed)) {
      update('maxComments', parsed);
    }
  }

  function handleMaxCommentsBlur() {
    const parsed = Number(maxCommentsInput);
    const clamped = Number.isNaN(parsed)
      ? options.maxComments
      : Math.min(MAX_COMMENTS_MAX, Math.max(MAX_COMMENTS_MIN, parsed));
    setMaxCommentsInput(String(clamped));
    if (clamped !== options.maxComments) update('maxComments', clamped);
  }

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-5 p-0">
        <p className="text-sm font-medium text-text-muted">{t('newAnalysis.configTitle')}</p>

        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium text-text-primary">{t('newAnalysis.analysisMode.label')}</label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                update('mode', 'single');
              }}
              className={`rounded-sm border px-4 py-2.5 text-sm font-medium transition-colors ${
                options.mode === 'single'
                  ? 'border-brand-400 bg-brand-500/10 text-text-primary'
                  : 'border-border-default bg-background-surface text-text-secondary hover:border-border-default'
              }`}
            >
              {t('newAnalysis.analysisMode.single')}
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                update('mode', 'compare');
              }}
              className={`rounded-sm border px-4 py-2.5 text-sm font-medium transition-colors ${
                options.mode === 'compare'
                  ? 'border-brand-400 bg-brand-500/10 text-text-primary'
                  : 'border-border-default bg-background-surface text-text-secondary hover:border-border-default'
              }`}
            >
              {t('newAnalysis.analysisMode.compare')}
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-2 border-t border-border-subtle pt-4">
          <label className="text-sm font-medium text-text-primary">{t('newAnalysis.sentimentEngine.label')}</label>
          <div className="grid grid-cols-3 gap-3">
            {SENTIMENT_ENGINE_OPTIONS.map((engine) => (
              <button
                key={engine.value}
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  update('sentimentEngine', engine.value);
                }}
                className={`rounded-sm border px-3 py-2.5 text-sm font-medium transition-colors ${
                  options.sentimentEngine === engine.value
                    ? 'border-brand-400 bg-brand-500/10 text-text-primary'
                    : 'border-border-default bg-background-surface text-text-secondary hover:border-border-default'
                }`}
              >
                {t(engine.labelKey)}
              </button>
            ))}
          </div>
          <p className="text-xs text-text-muted">
            {t(SENTIMENT_ENGINE_OPTIONS.find((e) => e.value === options.sentimentEngine)?.descKey ?? '')}
          </p>
          {(options.sentimentEngine === 'hybrid' || options.sentimentEngine === 'smart') && (
            <div className="flex items-start gap-2 rounded-sm border border-feedback-info/20 bg-feedback-info/5 px-3 py-2.5">
              <Clock className="mt-0.5 h-3.5 w-3.5 shrink-0 text-feedback-info" />
              <p className="text-xs italic leading-relaxed text-text-secondary">
                {t('newAnalysis.sentimentEngine.processingNotice')}
              </p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 border-t border-border-subtle pt-4">
          <div className="flex flex-col gap-1.5">
            <label htmlFor="max-comments" className="text-sm font-medium text-text-primary">
              {t('newAnalysis.maxComments.label')}
            </label>
            <div className="flex items-center gap-3">
              <Input
                id="max-comments"
                type="number"
                min={MAX_COMMENTS_MIN}
                max={MAX_COMMENTS_MAX}
                step={50}
                disabled={options.analyzeAllComments}
                value={maxCommentsInput}
                onChange={handleMaxCommentsChange}
                onBlur={handleMaxCommentsBlur}
                className="flex-1"
              />
              <div className="flex shrink-0 items-center pt-1">
                <Checkbox
                  id="analyzeAllComments"
                  label={t('newAnalysis.maxComments.all')}
                  checked={options.analyzeAllComments}
                  onChange={(e) => update('analyzeAllComments', e.target.checked)}
                />
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label htmlFor="sortOrder" className="text-sm font-medium text-text-primary">
              {t('newAnalysis.sorting.label')}
            </label>
            <select
              id="sortOrder"
              value={options.sortOrder}
              onChange={(e) => update('sortOrder', e.target.value as CommentSortOrder)}
              className="w-full rounded-sm border border-border-default bg-background-surface px-3.5 py-2.5 text-sm text-text-primary transition-colors duration-150 focus:border-brand-400"
            >
              <option value="relevance">{t('newAnalysis.sorting.relevance')}</option>
              <option value="time">{t('newAnalysis.sorting.time')}</option>
            </select>
          </div>

          <div className="flex items-center sm:col-span-2 pt-1">
            <Checkbox
              id="includeReplies"
              label={t('newAnalysis.includeReplies')}
              checked={options.includeReplies}
              onChange={(e) => update('includeReplies', e.target.checked)}
            />
          </div>
        </div>

        <div className="flex flex-col gap-1.5 border-t border-border-subtle pt-4">
          <label htmlFor="language" className="text-sm font-medium text-text-primary">
            {t('newAnalysis.languagePref.label')}
          </label>
          <select
            id="language"
            value={options.language}
            onChange={(e) => update('language', e.target.value as Language)}
            className="w-full rounded-sm border border-border-default bg-background-surface px-3.5 py-2.5 text-sm text-text-primary transition-colors duration-150 focus:border-brand-400"
          >
            <option value="auto">{t('newAnalysis.languagePref.auto')}</option>
            <option value="ar">{t('newAnalysis.languagePref.ar')}</option>
            <option value="en">{t('newAnalysis.languagePref.en')}</option>
          </select>
        </div>

        <div className="flex flex-col gap-3 border-t border-border-subtle pt-4">
          <label className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-1">
            {t('newAnalysis.nlpFeatures.title')}
          </label>
          {TOGGLE_FIELDS.map((field) => (
            <Checkbox
              key={field.key}
              id={field.key}
              label={t(field.labelKey)}
              checked={options[field.key] as boolean}
              onChange={(e) => update(field.key, e.target.checked as AnalysisOptionsState[typeof field.key])}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}