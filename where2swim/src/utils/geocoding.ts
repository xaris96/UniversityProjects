import { fetchWithTimeout } from './net';
import { findNearbyBeaches } from './overpass';
import { haversineKm } from './geo';
import { formatKm } from './format';

export interface GeocodeResult {
  name: string;
  label: string;
  latitude: number;
  longitude: number;
  isNearby?: boolean;
}

interface PhotonFeature {
  properties?: {
    name?: string;
    city?: string;
    district?: string;
    state?: string;
    osm_value?: string;
  };
  geometry?: {
    coordinates?: [number, number];
  };
}

const RESULT_LIMIT = 8;
const NEARBY_RADIUS_METERS = 8000;

function toGeocodeResult(feature: PhotonFeature): GeocodeResult | null {
  const props = feature.properties ?? {};
  const [longitude, latitude] = feature.geometry?.coordinates ?? [null, null];
  if (typeof latitude !== 'number' || typeof longitude !== 'number') return null;
  if (!props.name) return null;

  const parts = [props.name, props.city ?? props.district, props.state].filter(Boolean);
  return {
    name: props.name,
    label: parts.join(', '),
    latitude,
    longitude,
  };
}

async function searchBeachesByName(query: string): Promise<GeocodeResult[]> {
  // Ask for a large pool, since we then strictly keep only results
  // actually tagged as a beach in OpenStreetMap (`natural=beach`) — cuts
  // out hotels, restaurants, villages, bus stops etc. that share the same
  // name.
  const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&limit=30&bbox=23.3,34.6,26.5,35.8`;
  const response = await fetchWithTimeout(url, 8000);
  if (!response.ok) return [];

  const data = await response.json();
  const features: PhotonFeature[] = Array.isArray(data?.features) ? data.features : [];
  const beachFeatures = features.filter((f) => f.properties?.osm_value === 'beach');

  const results: GeocodeResult[] = [];
  for (const feature of beachFeatures) {
    const result = toGeocodeResult(feature);
    if (result) results.push(result);
    if (results.length >= RESULT_LIMIT) break;
  }
  return results;
}

async function geocodeAnyPlace(query: string): Promise<{ latitude: number; longitude: number } | null> {
  const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&limit=1&bbox=23.3,34.6,26.5,35.8`;
  try {
    const response = await fetchWithTimeout(url, 8000);
    if (!response.ok) return null;
    const data = await response.json();
    const [longitude, latitude] = data?.features?.[0]?.geometry?.coordinates ?? [null, null];
    if (typeof latitude !== 'number' || typeof longitude !== 'number') return null;
    return { latitude, longitude };
  } catch {
    return null;
  }
}

// Beaches near a general area (village/town/region) the user typed, sorted
// by distance — e.g. searching "Μπαλί" (a village, not itself tagged as a
// beach in OSM) surfaces the real named beaches nearby it instead of
// showing nothing.
async function searchBeachesNearArea(query: string): Promise<GeocodeResult[]> {
  const area = await geocodeAnyPlace(query);
  if (!area) return [];

  const nearby = await findNearbyBeaches(area.latitude, area.longitude, NEARBY_RADIUS_METERS);

  return nearby
    .map((beach) => ({
      name: beach.name,
      label: `${beach.name} (~${formatKm(haversineKm(area.latitude, area.longitude, beach.latitude, beach.longitude))} χλμ)`,
      latitude: beach.latitude,
      longitude: beach.longitude,
      distanceKm: haversineKm(area.latitude, area.longitude, beach.latitude, beach.longitude),
    }))
    .sort((a, b) => a.distanceKm - b.distanceKm)
    .slice(0, RESULT_LIMIT)
    .map(({ name, label, latitude, longitude }) => ({ name, label, latitude, longitude, isNearby: true }));
}

// Photon (built on OSM data) is designed for live, typo-tolerant
// autocomplete search — a better fit here than plain Nominatim, which
// expects a fairly complete/exact query. Free public API, fine for
// low-volume hobby use.
export async function searchCreteLocations(query: string): Promise<GeocodeResult[]> {
  const trimmed = query.trim();
  if (trimmed.length < 2) return [];

  const exact = await searchBeachesByName(trimmed);

  // A handful of exact-name matches is enough on its own. Otherwise (few
  // or no exact matches — e.g. "Μπαλί" isn't itself tagged as a beach)
  // also pull in real beaches near that general area, so the person still
  // gets useful options instead of a dead end.
  if (exact.length >= 3) return exact;

  const nearby = await searchBeachesNearArea(trimmed);
  const seen = new Set(exact.map((r) => `${r.latitude.toFixed(3)},${r.longitude.toFixed(3)}`));
  const combined = [...exact];
  for (const result of nearby) {
    const key = `${result.latitude.toFixed(3)},${result.longitude.toFixed(3)}`;
    if (seen.has(key)) continue;
    seen.add(key);
    combined.push(result);
    if (combined.length >= RESULT_LIMIT) break;
  }
  return combined;
}
