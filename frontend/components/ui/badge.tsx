import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center gap-1.5 rounded-sm px-2.5 py-0.5 text-xs font-medium',
  {
    variants: {
      sentiment: {
        positive: 'bg-sentiment-positive/15 text-sentiment-positive',
        neutral: 'bg-sentiment-neutral/15 text-sentiment-neutral',
        negative: 'bg-sentiment-negative/15 text-sentiment-negative',
      },
      status: {
        success: 'bg-feedback-success/15 text-feedback-success',
        warning: 'bg-feedback-warning/15 text-feedback-warning',
        danger: 'bg-feedback-danger/15 text-feedback-danger',
        info: 'bg-feedback-info/15 text-feedback-info',
      },
    },
  }
);

type BadgeProps = React.HTMLAttributes<HTMLSpanElement> &
  (
    | ({ sentiment: NonNullable<VariantProps<typeof badgeVariants>['sentiment']> } & {
        status?: never;
      })
    | ({ status: NonNullable<VariantProps<typeof badgeVariants>['status']> } & {
        sentiment?: never;
      })
  );

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, sentiment, status, ...props }, ref) => (
    <span
      ref={ref}
      className={cn(badgeVariants({ sentiment, status }), className)}
      {...props}
    />
  )
);
Badge.displayName = 'Badge';

export { Badge, badgeVariants };