import { Loader2, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface FetchStatusProps {
  isLoading?: boolean;
  error?: string | null;
  loadingLabel?: string;
}

export function FetchStatus({ isLoading, error, loadingLabel = 'Loading…' }: FetchStatusProps) {
  if (isLoading) {
    return (
      <Card variant="glass" className="p-5">
        <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
          <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
          {loadingLabel}
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card variant="glass" className="border-feedback-danger/30 p-5">
        <CardContent
          role="alert"
          className="flex items-center gap-2.5 p-0 text-sm text-feedback-danger"
        >
          <AlertCircle className="h-4 w-4 shrink-0" />
          {error}
        </CardContent>
      </Card>
    );
  }

  return null;
}
