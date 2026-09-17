export type DistanceFilter = 'all' | 'within30' | 'within1h' | 'within2h';

export const DISTANCE_FILTER_MINUTES: Record<Exclude<DistanceFilter, 'all'>, number> = {
  within30: 30,
  within1h: 60,
  within2h: 120,
};

export type SortOption = 'conditions' | 'alphabetical' | 'distance' | 'temperature';
