import * as React from 'react';
import { cn } from '@/lib/utils';

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: React.ReactNode;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, id, ...props }, ref) => (
    <label htmlFor={id} className="flex cursor-pointer items-start gap-2.5 text-sm text-text-secondary">
      <input
        ref={ref}
        id={id}
        type="checkbox"
        className={cn(
          'mt-0.5 h-4 w-4 shrink-0 cursor-pointer rounded-sm border border-border-default bg-background-surface accent-brand-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus',
          className
        )}
        {...props}
      />
      <span>{label}</span>
    </label>
  )
);
Checkbox.displayName = 'Checkbox';