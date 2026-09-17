export type WaveLevelKey = 'calm' | 'light' | 'rough';

export interface WaveLevel {
  key: WaveLevelKey;
}

export function waveLevel(heightM: number): WaveLevel {
  if (heightM < 0.3) return { key: 'calm' };
  if (heightM < 0.6) return { key: 'light' };
  return { key: 'rough' };
}
