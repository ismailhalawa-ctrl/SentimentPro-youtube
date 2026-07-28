import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const inputVariants = cva(
  'w-full rounded-sm border bg-background-surface px-3.5 py-2.5 text-sm text-text-primary placeholder:text-text-muted transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-50',
  {
    variants: {
      state: {
        default: 'border-border-default focus:border-brand-400',
        error: 'border-feedback-danger focus:border-feedback-danger',
      },
    },
    defaultVariants: {
      state: 'default',
    },
  }
);

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement>,
    VariantProps<typeof inputVariants> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, state, ...props }, ref) => (
    <input ref={ref} className={cn(inputVariants({ state }), className)} {...props} />
  )
);
Input.displayName = 'Input';

export { Input, inputVariants };