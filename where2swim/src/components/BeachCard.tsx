import { ActivityIndicator, Alert, Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Beach } from '../types/beach';
import { BeachConditions } from '../hooks/useBeachForecastSeries';
import { BeachDistance } from '../hooks/useBeachDistances';
import { degreesToCompass, windLevel } from '../utils/wind';
import { waveLevel } from '../utils/wave';
import { formatDuration, formatKm } from '../utils/format';
import { useLocale } from '../i18n/LocaleContext';
import { useFavorites } from '../context/FavoritesContext';

export function BeachCard({
  beach,
  state,
  distance,
  isTopPick,
  dayLabel,
  onPress,
}: {
  beach: Beach;
  state: { loading: boolean; error: boolean; conditions: BeachConditions | null };
  distance: BeachDistance | null;
  isTopPick?: boolean;
  dayLabel?: string;
  onPress?: () => void;
}) {
  const { locale, strings } = useLocale();
  const { favorites, toggleFavorite } = useFavorites();
  const { loading, error, conditions } = state;
  const name = locale === 'el' ? beach.nameEl : beach.nameEn;
  const isFavorite = favorites.has(beach.id);

  return (
    <Pressable style={[styles.card, isTopPick && styles.topPickCard]} onPress={onPress}>
      <Pressable style={styles.favoriteButton} onPress={() => toggleFavorite(beach.id)} hitSlop={8}>
        <Ionicons name={isFavorite ? 'star' : 'star-outline'} size={22} color={isFavorite ? '#f0a500' : '#b7c8d1'} />
      </Pressable>

      {isTopPick && (
        <Text style={styles.topPickBadge}>
          ⭐ {strings.topPick}
          {dayLabel ? ` · ${dayLabel}` : ''}
        </Text>
      )}

      <View style={styles.header}>
        <Text style={[styles.name, styles.nameWithFavorite]}>{name}</Text>
        <Text style={styles.region}>
          {strings.prefectures[beach.prefecture]} · {strings.coasts[beach.coast]}
          {beach.status === 'pending'
            ? ` · ${strings.pendingBadge}`
            : beach.source === 'community'
              ? ` · ${strings.communityBadge}`
              : ''}
        </Text>
      </View>

      {loading && <ActivityIndicator style={styles.status} />}

      {error && <Text style={styles.errorText}>{strings.status.error}</Text>}

      {conditions && (
        <View style={styles.status}>
          {(() => {
            const level = windLevel(conditions.windSpeedKmh);
            return (
              <Text style={[styles.conditionText, { color: level.color }]}>
                {level.dot} {strings.wind[level.key]} · {Math.round(conditions.windSpeedKmh)} km/h{' '}
                {degreesToCompass(conditions.windDirectionDeg, locale)} · {Math.round(conditions.temperatureC)}°C
              </Text>
            );
          })()}
          {conditions.waveHeightM !== null && (
            <View style={styles.waveRow}>
              <Text style={styles.waveText}>
                🌊 {strings.wave[waveLevel(conditions.waveHeightM).key]} · {conditions.waveHeightM.toFixed(1)} m
              </Text>
              <Pressable
                hitSlop={8}
                onPress={() => Alert.alert(strings.waveInfo.title, strings.waveInfo.body)}
              >
                <Ionicons name="information-circle-outline" size={16} color="#8ba3b0" />
              </Pressable>
            </View>
          )}
          {distance && (
            <Text style={styles.distanceText}>
              📍{' '}
              {distance.drivingKm !== null && distance.drivingMinutes !== null
                ? `${formatKm(distance.drivingKm)} ${strings.distance.km} · ${formatDuration(distance.drivingMinutes, locale)} (${strings.distance.driving})`
                : `~${formatKm(distance.straightLineKm)} ${strings.distance.km} (${strings.distance.straightLine})`}
            </Text>
          )}
        </View>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 6,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  favoriteButton: {
    position: 'absolute',
    top: 12,
    right: 12,
    zIndex: 1,
  },
  nameWithFavorite: {
    paddingRight: 28,
  },
  topPickCard: {
    borderWidth: 2,
    borderColor: '#0b6e99',
  },
  topPickBadge: {
    fontSize: 12,
    fontWeight: '700',
    color: '#0b6e99',
    marginBottom: 6,
  },
  header: {
    marginBottom: 8,
  },
  name: {
    fontSize: 18,
    fontWeight: '700',
    color: '#123',
  },
  region: {
    fontSize: 13,
    color: '#678',
    marginTop: 2,
  },
  status: {
    marginTop: 4,
    alignItems: 'flex-start',
    gap: 4,
  },
  conditionText: {
    fontSize: 14,
    fontWeight: '600',
  },
  waveRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  waveText: {
    fontSize: 13,
    color: '#345',
  },
  distanceText: {
    fontSize: 13,
    color: '#345',
  },
  errorText: {
    fontSize: 13,
    color: '#999',
  },
});
