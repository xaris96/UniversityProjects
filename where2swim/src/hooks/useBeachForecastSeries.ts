import { useEffect, useRef, useState } from 'react';
import { Beach } from '../types/beach';
import { fetchWithTimeout, runWithConcurrency } from '../utils/net';

export interface BeachConditions {
  windSpeedKmh: number;
  windDirectionDeg: number;
  temperatureC: number;
  waveHeightM: number | null;
  uvIndex: number | null;
}

export interface BeachForecastSeries {
  times: string[]; // local ISO timestamps, e.g. "2026-09-17T13:00"
  windSpeedKmh: number[];
  windDirectionDeg: number[];
  temperatureC: number[];
  waveHeightM: (number | null)[];
  uvIndex: number[];
}

export interface SeriesState {
  loading: boolean;
  error: boolean;
  series: BeachForecastSeries | null;
}

type SeriesMap = Record<string, SeriesState>;

const MAX_CONCURRENT_BEACHES = 12;
const FORECAST_DAYS = 6;

async function fetchWindSeries(beach: Beach) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${beach.latitude}&longitude=${beach.longitude}&hourly=wind_speed_10m,wind_direction_10m,temperature_2m,uv_index&wind_speed_unit=kmh&forecast_days=${FORECAST_DAYS}&timezone=auto`;
  const response = await fetchWithTimeout(url);
  if (!response.ok) throw new Error('wind request failed');
  const data = await response.json();
  return {
    times: data.hourly.time as string[],
    windSpeedKmh: data.hourly.wind_speed_10m as number[],
    windDirectionDeg: data.hourly.wind_direction_10m as number[],
    temperatureC: data.hourly.temperature_2m as number[],
    uvIndex: (data.hourly.uv_index as number[]) ?? [],
  };
}

async function fetchWaveSeries(beach: Beach): Promise<{ times: string[]; waveHeightM: number[] } | null> {
  try {
    const url = `https://marine-api.open-meteo.com/v1/marine?latitude=${beach.latitude}&longitude=${beach.longitude}&hourly=wave_height&forecast_days=${FORECAST_DAYS}&timezone=auto`;
    const response = await fetchWithTimeout(url);
    if (!response.ok) return null;
    const data = await response.json();
    if (!Array.isArray(data?.hourly?.time) || !Array.isArray(data?.hourly?.wave_height)) return null;
    return { times: data.hourly.time as string[], waveHeightM: data.hourly.wave_height as number[] };
  } catch {
    return null;
  }
}

async function fetchSeries(beach: Beach): Promise<BeachForecastSeries> {
  const [wind, wave] = await Promise.all([fetchWindSeries(beach), fetchWaveSeries(beach)]);

  const waveByTime = new Map<string, number>();
  if (wave) {
    wave.times.forEach((t, i) => waveByTime.set(t, wave.waveHeightM[i]));
  }

  return {
    times: wind.times,
    windSpeedKmh: wind.windSpeedKmh,
    windDirectionDeg: wind.windDirectionDeg,
    temperatureC: wind.temperatureC,
    waveHeightM: wind.times.map((t) => waveByTime.get(t) ?? null),
    uvIndex: wind.uvIndex,
  };
}

export function useBeachForecastSeries(beaches: Beach[]) {
  const [state, setState] = useState<SeriesMap>({});
  const [reloadKey, setReloadKey] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  const knownIdsRef = useRef<Set<string>>(new Set());
  const forceRefreshRef = useRef(false);

  useEffect(() => {
    let cancelled = false;
    const forceAll = forceRefreshRef.current;
    forceRefreshRef.current = false;

    // On a manual refresh, re-fetch every beach currently in the list.
    // Otherwise, only fetch beaches we haven't seen yet (e.g. a beach
    // that was just added), so switching filters/dates never re-triggers
    // network calls for beaches we already have data for.
    const targets = forceAll ? beaches : beaches.filter((b) => !knownIdsRef.current.has(b.id));

    if (targets.length === 0) {
      setRefreshing(false);
      return;
    }

    setState((prev) => {
      const next = { ...prev };
      targets.forEach((b) => {
        next[b.id] = { loading: true, error: false, series: null };
      });
      return next;
    });

    runWithConcurrency(targets, MAX_CONCURRENT_BEACHES, async (beach) => {
      try {
        const series = await fetchSeries(beach);
        if (cancelled) return;
        // Only mark as "known" once the fetch actually completes. If this
        // effect gets cancelled mid-flight (e.g. the beach list changes
        // again while requests are still in flight), the beach is retried
        // on the next run instead of being silently stuck in "loading".
        knownIdsRef.current.add(beach.id);
        setState((prev) => ({ ...prev, [beach.id]: { loading: false, error: false, series } }));
      } catch {
        if (cancelled) return;
        knownIdsRef.current.add(beach.id);
        setState((prev) => ({ ...prev, [beach.id]: { loading: false, error: true, series: null } }));
      }
    }).finally(() => {
      if (!cancelled) setRefreshing(false);
    });

    return () => {
      cancelled = true;
    };
  }, [beaches, reloadKey]);

  const refresh = () => {
    forceRefreshRef.current = true;
    setRefreshing(true);
    setReloadKey((k) => k + 1);
  };

  return { series: state, refresh, refreshing };
}
