import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const textareaVariants = cva(
  'w-full resize-y rounded-sm border bg-background-surface px-3.5 py-2.5 text-sm text-text-primary placeholder:text-text-muted transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-50',
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

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement>,
    VariantProps<typeof textareaVariants> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, state, rows = 5, ...props }, ref) => (
    <textarea ref={ref} rows={rows} className={cn(textareaVariants({ state }), className)} {...props} />
  )
);
Textarea.displayName = 'Textarea';

export { Textarea, textareaVariants };
