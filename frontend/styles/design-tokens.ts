
export const colors = {
  background: {
    base: '#0A0A0B',
    surface: '#141416',
    elevated: '#1C1C1F',
    overlay: 'rgba(0, 0, 0, 0.6)',
  },
  border: {
    default: '#27272A',
    subtle: '#1F1F22',
    focus: '#3B82F6',
  },
  text: {
    primary: '#FAFAFA',
    secondary: '#A1A1AA',
    muted: '#71717A',
    inverse: '#0A0A0B',
  },
  brand: {
    400: '#818CF8',
    500: '#6366F1',
    600: '#4F46E5',
  },
  sentiment: {
    positive: '#22C55E',
    neutral: '#A1A1AA',
    negative: '#EF4444',
  },
  feedback: {
    success: '#22C55E',
    warning: '#EAB308',
    danger: '#EF4444',
    info: '#3B82F6',
  },
} as const;

export const gradients = {
  brand: 'linear-gradient(135deg, #6366F1 0%, #818CF8 100%)',
  surface: 'linear-gradient(180deg, #1C1C1F 0%, #141416 100%)',
  radialGlow: 'radial-gradient(circle at 50% 0%, rgba(99,102,241,0.15), transparent 70%)',
} as const;

export const typography = {
  fontFamily: {
    sans: ['Inter', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  scale: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
  },
  weight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
} as const;

export const radius = {
  sm: '0.375rem',
  md: '0.5rem',
  lg: '0.75rem',
  xl: '1rem',
  full: '9999px',
} as const;

export const shadow = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.4)',
  md: '0 4px 12px rgba(0, 0, 0, 0.5)',
  lg: '0 8px 24px rgba(0, 0, 0, 0.6)',
  glow: {
    brand: '0 0 20px rgba(99, 102, 241, 0.35)',
    positive: '0 0 16px rgba(34, 197, 94, 0.25)',
    negative: '0 0 16px rgba(239, 68, 68, 0.25)',
  },
} as const;