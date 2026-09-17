import { useMemo } from 'react';
import { Alert, Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { Ionicons } from '@expo/vector-icons';
import { Beach } from '../types/beach';
import { BeachDistance } from '../hooks/useBeachDistances';
import { useBeachForecastSeries } from '../hooks/useBeachForecastSeries';
import { pickConditionsForOffset, formatDayLabel } from '../utils/forecastSelect';
import { degreesToCompass, windLevel } from '../utils/wind';
import { waveLevel } from '../utils/wave';
import { uvLevel } from '../utils/uv';
import { formatDuration, formatKm } from '../utils/format';
import { openDirections, shareBeach } from '../utils/navigation';
import { useLocale } from '../i18n/LocaleContext';
import { useFavorites } from '../context/FavoritesContext';

const DAY_OFFSETS = [0, 1, 2, 3, 4];

export function BeachDetailScreen({
  beach,
  distance,
  dayOffset,
  onClose,
}: {
  beach: Beach | null;
  distance: BeachDistance | null;
  dayOffset: number;
  onClose: () => void;
}) {
  const { locale, strings } = useLocale();
  const { favorites, toggleFavorite } = useFavorites();

  const beaches = useMemo(() => (beach ? [beach] : []), [beach]);
  const { series: seriesMap } = useBeachForecastSeries(beaches);

  if (!beach) return null;

  const name = locale === 'el' ? beach.nameEl : beach.nameEn;
  const isFavorite = favorites.has(beach.id);
  const entry = seriesMap[beach.id];
  const conditions = entry?.series ? pickConditionsForOffset(entry.series, dayOffset) : null;
  const level = conditions ? windLevel(conditions.windSpeedKmh) : null;

  return (
    <Modal visible={!!beach} animationType="slide" onRequestClose={onClose}>
      <View style={styles.container}>
        <View style={styles.headerRow}>
          <Text style={styles.title} numberOfLines={2}>
            {name}
          </Text>
          <Pressable onPress={onClose} hitSlop={8}>
            <Text style={styles.closeText}>✕</Text>
          </Pressable>
        </View>

        <ScrollView contentContainerStyle={styles.scrollContent}>
          <Text style={styles.region}>
            {strings.prefectures[beach.prefecture]} · {strings.coasts[beach.coast]}
            {beach.status === 'pending'
              ? ` · ${strings.pendingBadge}`
              : beach.source === 'community'
                ? ` · ${strings.communityBadge}`
                : ''}
          </Text>

          <MapView
            style={styles.map}
            pointerEvents="none"
            initialRegion={{
              latitude: beach.latitude,
              longitude: beach.longitude,
              latitudeDelta: 0.08,
              longitudeDelta: 0.08,
            }}
          >
            <Marker coordinate={{ latitude: beach.latitude, longitude: beach.longitude }} />
          </MapView>

          {entry?.loading && <Text style={styles.hint}>{strings.status.loading}</Text>}
          {entry?.error && <Text style={styles.hint}>{strings.status.error}</Text>}

          {conditions && level && (
            <View style={styles.conditionsBox}>
              <Text style={[styles.conditionMain, { color: level.color }]}>
                {level.dot} {strings.wind[level.key]} · {Math.round(conditions.windSpeedKmh)} km/h{' '}
                {degreesToCompass(conditions.windDirectionDeg, locale)}
              </Text>
              <Text style={styles.conditionSub}>🌡️ {Math.round(conditions.temperatureC)}°C</Text>
              {conditions.waveHeightM !== null && (
                <Text style={styles.conditionSub}>
                  🌊 {strings.wave[waveLevel(conditions.waveHeightM).key]} · {conditions.waveHeightM.toFixed(1)} m
                </Text>
              )}
              {conditions.uvIndex !== null && (
                <Text style={[styles.conditionSub, { color: uvLevel(conditions.uvIndex).color }]}>
                  ☀️ {strings.uv.label}: {Math.round(conditions.uvIndex)} ({strings.uv[uvLevel(conditions.uvIndex).key]})
                </Text>
              )}
              {distance && (
                <Text style={styles.conditionSub}>
                  📍{' '}
                  {distance.drivingKm !== null && distance.drivingMinutes !== null
                    ? `${formatKm(distance.drivingKm)} ${strings.distance.km} · ${formatDuration(distance.drivingMinutes, locale)} (${strings.distance.driving})`
                    : `~${formatKm(distance.straightLineKm)} ${strings.distance.km} (${strings.distance.straightLine})`}
                </Text>
              )}
            </View>
          )}

          {entry?.series && (
            <View style={styles.weekSection}>
              <Text style={styles.sectionLabel}>{strings.detail.weekGlance}</Text>
              <View style={styles.weekRow}>
                {DAY_OFFSETS.map((offset) => {
                  const dayConditions = pickConditionsForOffset(entry.series!, offset);
                  const dayLevel = dayConditions ? windLevel(dayConditions.windSpeedKmh) : null;
                  const label = formatDayLabel(offset, locale, strings.dateSelector.today, strings.dateSelector.tomorrow);
                  return (
                    <View key={offset} style={[styles.weekDay, offset === dayOffset && styles.weekDayActive]}>
                      <Text style={styles.weekDayLabel}>{label}</Text>
                      <Text style={styles.weekDayDot}>{dayLevel?.dot ?? '·'}</Text>
                      <Text style={styles.weekDayTemp}>
                        {dayConditions ? `${Math.round(dayConditions.temperatureC)}°` : '—'}
                      </Text>
                    </View>
                  );
                })}
              </View>
            </View>
          )}

          <View style={styles.actionsRow}>
            <Pressable style={styles.actionButton} onPress={() => openDirections(beach)}>
              <Ionicons name="navigate-outline" size={18} color="#fff" />
              <Text style={styles.actionButtonText}>{strings.detail.directions}</Text>
            </Pressable>
            <Pressable
              style={[styles.actionButton, styles.actionButtonSecondary]}
              onPress={() => shareBeach(beach, locale)}
            >
              <Ionicons name="share-social-outline" size={18} color="#0b6e99" />
              <Text style={[styles.actionButtonText, styles.actionButtonTextSecondary]}>{strings.detail.share}</Text>
            </Pressable>
            <Pressable
              style={[styles.actionButton, styles.actionButtonSecondary]}
              onPress={() => toggleFavorite(beach.id)}
            >
              <Ionicons name={isFavorite ? 'star' : 'star-outline'} size={18} color="#f0a500" />
              <Text style={[styles.actionButtonText, styles.actionButtonTextSecondary]}>
                {isFavorite ? strings.detail.unfavorite : strings.detail.favorite}
              </Text>
            </Pressable>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#eef7fb',
    paddingTop: 56,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: 20,
    marginBottom: 12,
    gap: 12,
  },
  title: {
    flex: 1,
    fontSize: 24,
    fontWeight: '700',
    color: '#0b6e99',
  },
  closeText: {
    fontSize: 22,
    color: '#33586b',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 32,
  },
  region: {
    fontSize: 13,
    color: '#678',
    marginBottom: 12,
  },
  map: {
    height: 180,
    borderRadius: 12,
    marginBottom: 16,
  },
  hint: {
    fontSize: 13,
    color: '#678',
    marginBottom: 12,
  },
  conditionsBox: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    gap: 6,
    marginBottom: 16,
  },
  conditionMain: {
    fontSize: 16,
    fontWeight: '700',
  },
  conditionSub: {
    fontSize: 14,
    color: '#345',
  },
  weekSection: {
    marginBottom: 20,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#33586b',
    marginBottom: 8,
  },
  weekRow: {
    flexDirection: 'row',
    gap: 8,
  },
  weekDay: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
    gap: 4,
  },
  weekDayActive: {
    borderWidth: 2,
    borderColor: '#0b6e99',
  },
  weekDayLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#33586b',
  },
  weekDayDot: {
    fontSize: 14,
  },
  weekDayTemp: {
    fontSize: 12,
    color: '#678',
  },
  actionsRow: {
    flexDirection: 'row',
    gap: 10,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    backgroundColor: '#0b6e99',
    borderRadius: 12,
    paddingVertical: 12,
  },
  actionButtonSecondary: {
    backgroundColor: '#dcebf2',
  },
  actionButtonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 13,
  },
  actionButtonTextSecondary: {
    color: '#0b6e99',
  },
});
