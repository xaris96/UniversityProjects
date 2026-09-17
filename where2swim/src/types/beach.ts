export type Coast = 'N' | 'S' | 'E' | 'W';
export type Prefecture = 'chania' | 'rethymno' | 'heraklion' | 'lasithi';

export interface Beach {
  id: string;
  nameEl: string;
  nameEn: string;
  prefecture: Prefecture;
  coast: Coast;
  latitude: number;
  longitude: number;
  source?: 'curated' | 'community';
  status?: 'pending' | 'approved';
}
