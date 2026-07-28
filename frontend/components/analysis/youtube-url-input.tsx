'use client';

import { AlertCircle, CheckCircle2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { FormField } from '@/components/forms/form-field';
import { useLanguage } from '@/lib/i18n/language-provider';

const YOUTUBE_URL_PATTERN =
  /^(https?:\/\/)?(www\.|m\.)?(youtube\.com\/(watch\?v=|shorts\/|embed\/)|youtu\.be\/)[\w-]{11}(&\S*|\?\S*)?$/;

export function isValidYouTubeUrl(url: string): boolean {
  return YOUTUBE_URL_PATTERN.test(url.trim());
}

interface YouTubeUrlInputProps {
  value: string;
  onChange: (value: string) => void;
  id?: string;
  label?: string;
}

export function YouTubeUrlInput({
  value,
  onChange,
  id = 'youtube-url',
  label = 'YouTube Video URL',
}: YouTubeUrlInputProps) {
  const { t } = useLanguage();
  const isValid = value.trim().length > 0 && isValidYouTubeUrl(value);
  const showError = value.trim().length > 0 && !isValid;
  const errorMessage = showError ? t('common.invalidYoutubeUrl') : undefined;

  return (
    <FormField label={label} htmlFor={id} error={errorMessage}>
      <div className="relative">
        <Input
          id={id}
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          state={showError ? 'error' : 'default'}
          aria-invalid={showError}
          aria-describedby={showError ? `${id}-error` : undefined}
          className="pe-10"
        />
        {value.trim().length > 0 && (
          <span className="absolute end-3 top-1/2 -translate-y-1/2">
            {isValid ? (
              <CheckCircle2 className="h-4 w-4 text-sentiment-positive" />
            ) : (
              <AlertCircle className="h-4 w-4 text-feedback-danger" />
            )}
          </span>
        )}
      </div>
    </FormField>
  );
}
