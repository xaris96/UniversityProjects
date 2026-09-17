import { BeachConditions, BeachForecastSeries } from '../hooks/useBeachForecastSeries';
import { Locale } from '../i18n/translations';

// "Today" uses the hour closest to right now; future days use a fixed
// early-afternoon hour, since that's roughly when most people would head
// to the beach and it avoids picking a stale early-morning reading.
const DAYTIME_HOUR = 13;

function formatLocalDate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function pickConditionsForOffset(series: BeachForecastSeries, dayOffset: number): BeachConditions | null {
  const targetDate = new Date();
  targetDate.setDate(targetDate.getDate() + dayOffset);
  const dateStr = formatLocalDate(targetDate);
  const targetHour = dayOffset === 0 ? new Date().getHours() : DAYTIME_HOUR;
  const hourStr = String(targetHour).padStart(2, '0');

  let index = series.times.findIndex((t) => t.startsWith(`${dateStr}T${hourStr}:`));
  if (index === -1) {
    // Fall back to any hour available for that date.
    index = series.times.findIndex((t) => t.startsWith(dateStr));
  }
  if (index === -1) return null;

  return {
    windSpeedKmh: series.windSpeedKmh[index],
    windDirectionDeg: series.windDirectionDeg[index],
    temperatureC: series.temperatureC[index],
    waveHeightM: series.waveHeightM[index] ?? null,
    uvIndex: series.uvIndex[index] ?? null,
  };
}

const WEEKDAYS_EL = ['Κυρ', 'Δευ', 'Τρί', 'Τετ', 'Πέμ', 'Παρ', 'Σάβ'];
const WEEKDAYS_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function formatDayLabel(dayOffset: number, locale: Locale, todayLabel: string, tomorrowLabel: string): string {
  if (dayOffset === 0) return todayLabel;
  if (dayOffset === 1) return tomorrowLabel;
  const date = new Date();
  date.setDate(date.getDate() + dayOffset);
  const names = locale === 'el' ? WEEKDAYS_EL : WEEKDAYS_EN;
  return names[date.getDay()];
}
