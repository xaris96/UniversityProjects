const COMPASS_POINTS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
const COMPASS_POINTS_EL = ['Β', 'ΒΑ', 'Α', 'ΝΑ', 'Ν', 'ΝΔ', 'Δ', 'ΒΔ'];

export function degreesToCompass(deg: number, locale: 'el' | 'en' = 'el'): string {
  const index = Math.round(deg / 45) % 8;
  return locale === 'el' ? COMPASS_POINTS_EL[index] : COMPASS_POINTS[index];
}

export type WindLevelKey = 'calm' | 'moderate' | 'strong';

export interface WindLevel {
  key: WindLevelKey;
  dot: string;
  color: string;
}

export function windLevel(speedKmh: number): WindLevel {
  if (speedKmh < 15) return { key: 'calm', dot: '🟢', color: '#2e7d32' };
  if (speedKmh < 25) return { key: 'moderate', dot: '🟡', color: '#ef6c00' };
  return { key: 'strong', dot: '🔴', color: '#c62828' };
}
