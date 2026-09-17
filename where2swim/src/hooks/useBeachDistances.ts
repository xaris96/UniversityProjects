import { useEffect, useMemo, useState } from 'react';
import { Beach } from '../types/beach';
import { UserCoords } from './useUserLocation';
import { haversineKm } from '../utils/geo';
import { fetchWithTimeout } from '../utils/net';

export interface BeachDistance {
  straightLineKm: number;
  drivingKm: number | null;
  drivingMinutes: number | null;
}

type DistanceMap = Record<string, BeachDistance>;

export function useBeachDistances(userCoords: UserCoords | null, beaches: Beach[]) {
  const [driving, setDriving] = useState<Record<string, { km: number; minutes: number }> | null>(null);
  const [drivingLoading, setDrivingLoading] = useState(false);

  const straightLine = useMemo<Record<string, number>>(() => {
    if (!userCoords) return {};
    return Object.fromEntries(
      beaches.map((b) => [b.id, haversineKm(userCoords.latitude, userCoords.longitude, b.latitude, b.longitude)])
    );
  }, [userCoords, beaches]);

  useEffect(() => {
    if (!userCoords) {
      setDriving(null);
      return;
    }
    let cancelled = false;
    setDrivingLoading(true);

    async function fetchDrivingDistances() {
      try {
        const coordsParam = [
          `${userCoords!.longitude},${userCoords!.latitude}`,
          ...beaches.map((b) => `${b.longitude},${b.latitude}`),
        ].join(';');
        const destinations = beaches.map((_, i) => i + 1).join(';');
        const url = `https://router.project-osrm.org/table/v1/driving/${coordsParam}?sources=0&destinations=${destinations}&annotations=duration,distance`;
        const response = await fetchWithTimeout(url, 15000);
        if (!response.ok) throw new Error('routing request failed');
        const data = await response.json();
        if (cancelled) return;

        const durations: (number | null)[] = data.durations?.[0] ?? [];
        const distances: (number | null)[] = data.distances?.[0] ?? [];

        const result: Record<string, { km: number; minutes: number }> = {};
        beaches.forEach((beach, i) => {
          const durationSec = durations[i];
          const distanceM = distances[i];
          if (typeof durationSec === 'number' && typeof distanceM === 'number') {
            result[beach.id] = { km: distanceM / 1000, minutes: durationSec / 60 };
          }
        });
        setDriving(result);
      } catch {
        if (!cancelled) setDriving(null);
      } finally {
        if (!cancelled) setDrivingLoading(false);
      }
    }

    fetchDrivingDistances();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userCoords?.latitude, userCoords?.longitude, beaches]);

  const distances = useMemo<DistanceMap>(() => {
    return Object.fromEntries(
      beaches.map((b) => [
        b.id,
        {
          straightLineKm: straightLine[b.id] ?? 0,
          drivingKm: driving?.[b.id]?.km ?? null,
          drivingMinutes: driving?.[b.id]?.minutes ?? null,
        },
      ])
    );
  }, [beaches, straightLine, driving]);

  return { distances, drivingLoading };
}
