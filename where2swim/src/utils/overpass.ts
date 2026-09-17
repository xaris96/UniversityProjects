import { fetchWithTimeout } from './net';

export interface NearbyBeach {
  name: string;
  latitude: number;
  longitude: number;
}

interface OverpassElement {
  lat?: number;
  lon?: number;
  center?: { lat: number; lon: number };
  tags?: { name?: string; alt_name?: string; ['name:en']?: string };
}

// Public Overpass instances are flaky under load (504s are common), so we
// try a couple of independent ones in turn rather than giving up after one
// failure. Free, no key, fine for low-volume hobby use.
const OVERPASS_URLS = ['https://overpass.private.coffee/api/interpreter', 'https://overpass-api.de/api/interpreter'];

function parseElements(elements: OverpassElement[]): NearbyBeach[] {
  const seenNames = new Set<string>();
  const results: NearbyBeach[] = [];
  for (const el of elements) {
    const lat = el.lat ?? el.center?.lat;
    const lon = el.lon ?? el.center?.lon;
    const name = el.tags?.name ?? el.tags?.['name:en'] ?? el.tags?.alt_name;
    if (typeof lat !== 'number' || typeof lon !== 'number' || !name) continue;
    if (seenNames.has(name)) continue;
    seenNames.add(name);
    results.push({ name, latitude: lat, longitude: lon });
  }
  return results;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function findNearbyBeaches(
  latitude: number,
  longitude: number,
  radiusMeters = 5000
): Promise<NearbyBeach[]> {
  const query = `[out:json][timeout:12];(node["natural"="beach"](around:${radiusMeters},${latitude},${longitude});way["natural"="beach"](around:${radiusMeters},${latitude},${longitude}););out center tags;`;

  // Both public mirrors can be flaky (frequent 504s under load), so this
  // goes through the whole list twice before giving up, rather than
  // failing after a single bad response from each.
  for (let pass = 0; pass < 2; pass++) {
    for (const url of OVERPASS_URLS) {
      try {
        const response = await fetchWithTimeout(url, 9000, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Where2Swim/1.0 (Crete beach conditions app)',
          },
          body: `data=${encodeURIComponent(query)}`,
        });
        if (!response.ok) continue;

        const data = await response.json();
        const elements: OverpassElement[] = Array.isArray(data?.elements) ? data.elements : [];
        return parseElements(elements);
      } catch {
        // try the next mirror
      }
    }
    if (pass === 0) await sleep(800);
  }

  return [];
}
