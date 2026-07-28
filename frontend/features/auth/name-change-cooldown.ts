const COOLDOWN_DAYS = 60;
const DAY_MS = 24 * 60 * 60 * 1000;

export function getNameChangeDaysRemaining(lastNameChange: string | null): number {
  if (!lastNameChange) return 0;
  const cooldownEnds = new Date(lastNameChange).getTime() + COOLDOWN_DAYS * DAY_MS;
  const remainingMs = cooldownEnds - Date.now();
  return remainingMs > 0 ? Math.ceil(remainingMs / DAY_MS) : 0;
}
