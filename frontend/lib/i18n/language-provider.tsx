'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { translations, type Locale } from './translations';

interface LanguageContextValue {
  language: Locale;
  setLanguage: (lang: Locale) => void;
  dir: 'ltr' | 'rtl';
  t: (path: string, params?: Record<string, string | number>) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

const STORAGE_KEY = 'sentimentpro-language';

function resolvePath(tree: unknown, path: string): unknown {
  return path.split('.').reduce<unknown>((node, segment) => {
    if (node && typeof node === 'object' && segment in (node as Record<string, unknown>)) {
      return (node as Record<string, unknown>)[segment];
    }
    return undefined;
  }, tree);
}

function interpolate(template: string, params?: Record<string, string | number>): string {
  if (!params) return template;
  return template.replace(/\{(\w+)\}/g, (match, key) => (key in params ? String(params[key]) : match));
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Locale>('en');

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored === 'ar' || stored === 'en') {
      setLanguageState(stored);
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
  }, [language]);

  function setLanguage(lang: Locale) {
    setLanguageState(lang);
    window.localStorage.setItem(STORAGE_KEY, lang);
  }

  function t(path: string, params?: Record<string, string | number>): string {
    const value = resolvePath(translations[language], path) ?? resolvePath(translations.en, path);
    return typeof value === 'string' ? interpolate(value, params) : path;
  }

  return (
    <LanguageContext.Provider
      value={{ language, setLanguage, dir: language === 'ar' ? 'rtl' : 'ltr', t }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextValue {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used within a LanguageProvider');
  return ctx;
}
