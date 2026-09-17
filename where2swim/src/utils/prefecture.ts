import { Prefecture } from '../types/beach';

// Crete's four prefectures run roughly west-to-east as vertical strips,
// so longitude alone is a reasonable automatic guess. Users can still
// override it manually in the add-beach form.
export function inferPrefectureFromLongitude(longitude: number): Prefecture {
  if (longitude < 24.05) return 'chania';
  if (longitude < 24.75) return 'rethymno';
  if (longitude < 25.65) return 'heraklion';
  return 'lasithi';
}
