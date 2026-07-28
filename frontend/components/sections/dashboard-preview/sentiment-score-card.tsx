import { TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { MiniChart } from './mini-chart';

export function SentimentScoreCard() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-text-muted">Overall Sentiment</p>
            <p className="text-3xl font-bold text-text-primary">78.4%</p>
          </div>
          <div className="flex items-center gap-1 rounded-full bg-sentiment-positive/15 px-2.5 py-1 text-xs font-medium text-sentiment-positive">
            <TrendingUp className="h-3.5 w-3.5" />
            +4.2%
          </div>
        </div>
        <MiniChart />
      </CardContent>
    </Card>
  );
}