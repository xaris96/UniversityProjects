export type UvLevelKey = 'low' | 'moderate' | 'high' | 'veryHigh' | 'extreme';

export interface UvLevel {
  key: UvLevelKey;
  color: string;
}

// Standard WHO UV index bands.
export function uvLevel(index: number): UvLevel {
  if (index < 3) return { key: 'low', color: '#2e7d32' };
  if (index < 6) return { key: 'moderate', color: '#ef6c00' };
  if (index < 8) return { key: 'high', color: '#e65100' };
  if (index < 11) return { key: 'veryHigh', color: '#c62828' };
  return { key: 'extreme', color: '#7b1fa2' };
}
