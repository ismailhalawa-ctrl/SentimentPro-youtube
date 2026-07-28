'use client';

import { useEffect, useState } from 'react';

export interface DashboardPreferences {
  defaultLanguage: 'auto' | 'ar' | 'en';
  defaultMaxComments: number;
  compactLists: boolean;
}

const STORAGE_KEY = 'sentimentpro:dashboard-preferences';

export const DEFAULT_DASHBOARD_PREFERENCES: DashboardPreferences = {
  defaultLanguage: 'auto',
  defaultMaxComments: 500,
  compactLists: false,
};

export function loadDashboardPreferences(): DashboardPreferences {
  if (typeof window === 'undefined') return DEFAULT_DASHBOARD_PREFERENCES;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT_DASHBOARD_PREFERENCES;
    return { ...DEFAULT_DASHBOARD_PREFERENCES, ...JSON.parse(raw) };
  } catch {
    return DEFAULT_DASHBOARD_PREFERENCES;
  }
}

export function useDashboardPreferences() {
  const [preferences, setPreferencesState] = useState<DashboardPreferences>(
    DEFAULT_DASHBOARD_PREFERENCES
  );

  useEffect(() => {
    setPreferencesState(loadDashboardPreferences());
  }, []);

  function setPreferences(next: DashboardPreferences) {
    setPreferencesState(next);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  }

  return { preferences, setPreferences };
}
