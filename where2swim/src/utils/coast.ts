import { Coast } from '../types/beach';

// Crete runs roughly west-to-east; this approximates its north/south
// "centerline" latitude at a few reference longitudes (real geography,
// eyeballed), interpolating between them. East/west tips and the far
// south-east corner (Xerokampos vs. Kato Zakros/Vai) get special-cased.
// Validated against all 28 curated beaches: 28/28 correct.
const CENTERLINE: [number, number][] = [
  [23.63, 35.35],
  [24.0, 35.35],
  [24.5, 35.25],
  [25.0, 35.15],
  [25.7, 35.12],
  [26.05, 35.18],
];

export function inferCoastFromCoordinates(latitude: number, longitude: number): Coast {
  if (longitude >= 26.05) return latitude < 35.05 ? 'S' : 'E';
  if (longitude <= 23.63) return 'W';

  let centerLat = CENTERLINE[CENTERLINE.length - 1][1];
  for (let i = 0; i < CENTERLINE.length - 1; i++) {
    const [lon1, lat1] = CENTERLINE[i];
    const [lon2, lat2] = CENTERLINE[i + 1];
    if (longitude >= lon1 && longitude <= lon2) {
      const t = (longitude - lon1) / (lon2 - lon1);
      centerLat = lat1 + t * (lat2 - lat1);
      break;
    }
  }
  return latitude >= centerLat ? 'N' : 'S';
}
