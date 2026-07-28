import type { Config } from 'tailwindcss';
import { colors, gradients, typography, radius, shadow } from './styles/design-tokens';

const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: colors.background,
        border: colors.border,
        text: colors.text,
        brand: colors.brand,
        sentiment: colors.sentiment,
        feedback: colors.feedback,
      },
      backgroundImage: {
        'gradient-brand': gradients.brand,
        'gradient-surface': gradients.surface,
        'gradient-radial-glow': gradients.radialGlow,
      },
      fontFamily: {
        sans: [...typography.fontFamily.sans],
        mono: [...typography.fontFamily.mono],
      },
      fontSize: {
        xs: [typography.scale.xs[0], { ...typography.scale.xs[1] }],
        sm: [typography.scale.sm[0], { ...typography.scale.sm[1] }],
        base: [typography.scale.base[0], { ...typography.scale.base[1] }],
        lg: [typography.scale.lg[0], { ...typography.scale.lg[1] }],
        xl: [typography.scale.xl[0], { ...typography.scale.xl[1] }],
        '2xl': [typography.scale['2xl'][0], { ...typography.scale['2xl'][1] }],
        '3xl': [typography.scale['3xl'][0], { ...typography.scale['3xl'][1] }],
        '4xl': [typography.scale['4xl'][0], { ...typography.scale['4xl'][1] }],
      },
      fontWeight: { ...typography.weight },
      borderRadius: radius,
      boxShadow: {
        sm: shadow.sm,
        md: shadow.md,
        lg: shadow.lg,
        'glow-brand': shadow.glow.brand,
        'glow-positive': shadow.glow.positive,
        'glow-negative': shadow.glow.negative,
      },
    },
  },
  plugins: [],
};

export default config;