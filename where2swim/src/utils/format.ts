import { Locale } from '../i18n/translations';

export function formatDuration(minutes: number, locale: Locale): string {
  const totalMinutes = Math.round(minutes);
  const hours = Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;

  if (hours === 0) return locale === 'el' ? `${mins}′` : `${mins}m`;
  if (mins === 0) return locale === 'el' ? `${hours}ω` : `${hours}h`;
  return locale === 'el' ? `${hours}ω ${mins}′` : `${hours}h ${mins}m`;
}

export function formatKm(km: number): string {
  return km < 10 ? km.toFixed(1) : Math.round(km).toString();
}
