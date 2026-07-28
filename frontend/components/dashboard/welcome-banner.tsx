import type { User } from '@/features/auth/types';

export function WelcomeBanner({ user }: { user: User }) {
  const firstName = user.full_name.split(' ')[0];

  return (
    <div>
      <h1 className="text-2xl font-semibold text-text-primary">Welcome, {firstName}</h1>
      <p className="mt-1 text-sm text-text-secondary">
        Analyze YouTube comments with AI-powered sentiment, spam, sarcasm, and keyword detection.
      </p>
    </div>
  );
}
