import { Beach } from '../types/beach';
import { haversineKm } from './geo';
import { normalizeForSearch } from './transliteration';

const NEARBY_KM = 0.5;
const SAME_NAME_NEARBY_KM = 5;

export interface DuplicateCandidate {
  name: string;
  latitude: number;
  longitude: number;
}

// Flags a likely-duplicate submission: either physically very close to an
// existing beach (regardless of name), or a name match within a wider
// radius (catches the same beach entered with a slightly different name,
// or in a different script — e.g. Greek vs. a Latin-only OSM name).
export function findPossibleDuplicate(candidate: DuplicateCandidate, existing: Beach[]): Beach | null {
  const candidateName = normalizeForSearch(candidate.name);
  let closest: { beach: Beach; distanceKm: number } | null = null;

  for (const beach of existing) {
    const distanceKm = haversineKm(candidate.latitude, candidate.longitude, beach.latitude, beach.longitude);
    const nameMatches =
      normalizeForSearch(beach.nameEl) === candidateName || normalizeForSearch(beach.nameEn) === candidateName;

    const isDuplicate = distanceKm < NEARBY_KM || (distanceKm < SAME_NAME_NEARBY_KM && nameMatches);
    if (isDuplicate && (!closest || distanceKm < closest.distanceKm)) {
      closest = { beach, distanceKm };
    }
  }

  return closest?.beach ?? null;
}
