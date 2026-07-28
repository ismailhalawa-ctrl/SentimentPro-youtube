'use client';

import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Check, Globe } from 'lucide-react';
import { useLanguage } from '@/lib/i18n/language-provider';
import type { Locale } from '@/lib/i18n/translations';

const LANGUAGES: { value: Locale; nativeLabel: string }[] = [
  { value: 'en', nativeLabel: 'English' },
  { value: 'ar', nativeLabel: 'العربية' },
];

export function LanguageToggle() {
  const { language, setLanguage, t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }

    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') setIsOpen(false);
    }

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen]);

  return (
    <div ref={menuRef} className="relative">
      <button
        onClick={() => setIsOpen((v) => !v)}
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-label={t('languageToggle.label')}
        className="flex items-center gap-1.5 rounded-md p-2 text-text-secondary transition-colors hover:bg-background-elevated hover:text-text-primary"
      >
        <Globe className="h-4.5 w-4.5" />
        <span className="text-xs font-semibold uppercase">{language}</span>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            role="menu"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.15 }}
            className="absolute end-0 top-full z-50 mt-2 w-40 overflow-hidden rounded-lg border border-border-default bg-background-elevated shadow-lg"
          >
            <div className="p-1.5">
              {LANGUAGES.map((lang) => (
                <button
                  key={lang.value}
                  role="menuitem"
                  onClick={() => {
                    setLanguage(lang.value);
                    setIsOpen(false);
                  }}
                  className="flex w-full items-center justify-between gap-2.5 rounded-sm px-3 py-2 text-sm text-text-secondary transition-colors hover:bg-background-surface hover:text-text-primary"
                >
                  {lang.nativeLabel}
                  {language === lang.value && <Check className="h-3.5 w-3.5 text-brand-400" />}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
