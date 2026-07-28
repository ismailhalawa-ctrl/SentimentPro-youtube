import { cn } from '@/lib/utils';

function getStrength(password: string): { score: number; label: string } {
  if (!password) return { score: 0, label: '' };

  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const labels = ['Very weak', 'Weak', 'Fair', 'Good', 'Strong'];
  return { score, label: labels[Math.min(score, labels.length - 1)] };
}

export function PasswordStrength({ password }: { password: string }) {
  const { score, label } = getStrength(password);
  if (!password) return null;

  const colorClass =
    score <= 1
      ? 'bg-feedback-danger'
      : score <= 2
        ? 'bg-feedback-warning'
        : score <= 3
          ? 'bg-brand-400'
          : 'bg-sentiment-positive';

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex gap-1.5">
        {Array.from({ length: 5 }).map((_, i) => (
          <span
            key={i}
            className={cn(
              'h-1 flex-1 rounded-full bg-background-surface',
              i < score && colorClass
            )}
          />
        ))}
      </div>
      <p className="text-xs text-text-muted">{label}</p>
    </div>
  );
}