'use client';

import { Rocket } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useLanguage } from '@/lib/i18n/language-provider';

interface StartAnalysisButtonProps {
  isValid: boolean;
  isRunning: boolean;
  onClick: () => void;
}

export function StartAnalysisButton({ isValid, isRunning, onClick }: StartAnalysisButtonProps) {
  const { t } = useLanguage();
  return (
    <Button
      variant="primary"
      size="lg"
      onClick={onClick}
      disabled={!isValid || isRunning}
      isLoading={isRunning}
      className="w-full sm:w-auto"
    >
      {!isRunning && <Rocket className="h-4 w-4" />}
      {isRunning ? t('newAnalysis.startButton.analyzing') : t('newAnalysis.startButton.start')}
    </Button>
  );
}
