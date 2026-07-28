'use client';

import { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface ExtractionLoadingCardProps {
  label: string;
}

const SLOW_THRESHOLD_SECONDS = 8;

export function ExtractionLoadingCard({ label }: ExtractionLoadingCardProps) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setElapsedSeconds((s) => s + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const isSlow = elapsedSeconds >= SLOW_THRESHOLD_SECONDS;

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-1.5 p-0">
        <div className="flex items-center gap-2.5 text-sm text-text-secondary">
          <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
          {label}
        </div>
        {isSlow && (
          <p className="pl-[1.625rem] text-xs text-text-muted">
            Still working — larger comment sets can take up to a minute the first time.
          </p>
        )}
      </CardContent>
    </Card>
  );
}
