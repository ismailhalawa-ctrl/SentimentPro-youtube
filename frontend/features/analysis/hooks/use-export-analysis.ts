'use client';

import { useState } from 'react';
import { exportAnalysisJob } from '@/features/analysis/api/analysis-api';
import type { ExportFormat } from '@/features/analysis/types';

export function useExportAnalysis() {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function exportAs(jobId: number, format: ExportFormat, filenameHint: string) {
    setIsExporting(true);
    setError(null);
    try {
      const { blob, extension } = await exportAnalysisJob(jobId, format);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${filenameHint}.${extension}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch {
      setError(`Failed to export ${format.toUpperCase()}. Please try again.`);
    } finally {
      setIsExporting(false);
    }
  }

  return { exportAs, isExporting, error };
}
