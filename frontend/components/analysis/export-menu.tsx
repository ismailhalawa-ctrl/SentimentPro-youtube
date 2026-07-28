'use client';

import { useEffect, useRef, useState } from 'react';
import { ChevronDown, Download, FileSpreadsheet, FileText, FileType } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useExportAnalysis } from '@/features/analysis/hooks/use-export-analysis';
import type { ExportFormat } from '@/features/analysis/types';

const FORMATS: { format: ExportFormat; label: string; icon: typeof FileText }[] = [
  { format: 'csv', label: 'CSV', icon: FileText },
  { format: 'excel', label: 'Excel', icon: FileSpreadsheet },
  { format: 'pdf', label: 'PDF Report', icon: FileType },
];

interface ExportMenuProps {
  jobId: number;
  filenameHint: string;
}

export function ExportMenu({ jobId, filenameHint }: ExportMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const { exportAs, isExporting } = useExportAnalysis();

  useEffect(() => {
    if (!isOpen) return;
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setIsOpen(false);
    }
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        setIsOpen(false);
        triggerRef.current?.focus();
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen]);

  return (
    <div ref={menuRef} className="relative">
      <Button
        ref={triggerRef}
        variant="primary"
        size="sm"
        isLoading={isExporting}
        onClick={() => setIsOpen((v) => !v)}
        aria-expanded={isOpen}
        aria-haspopup="menu"
      >
        {!isExporting && <Download className="h-3.5 w-3.5" />} Export
        <ChevronDown className={`h-3.5 w-3.5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </Button>

      {isOpen && (
        <div
          role="menu"
          className="absolute right-0 top-full z-50 mt-2 w-44 overflow-hidden rounded-lg border border-border-default bg-background-elevated shadow-lg"
        >
          {FORMATS.map(({ format, label, icon: Icon }) => (
            <button
              key={format}
              role="menuitem"
              onClick={() => {
                setIsOpen(false);
                exportAs(jobId, format, filenameHint);
              }}
              className="flex w-full items-center gap-2.5 px-3.5 py-2.5 text-left text-sm text-text-secondary transition-colors hover:bg-background-surface hover:text-text-primary"
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
