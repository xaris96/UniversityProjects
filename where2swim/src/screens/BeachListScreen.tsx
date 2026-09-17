import { useMemo, useState } from 'react';
import { ActivityIndicator, FlatList, Pressable, RefreshControl, StyleSheet, Text, TextInput, View } from 'react-native';
import { BEACHES } from '../data/beaches';
import { BeachCard } from '../components/BeachCard';
import { FilterBar } from '../components/FilterBar';
import { LocationPrompt } from '../components/LocationPrompt';
import { SortSelector } from '../components/SortSelector';
import { BeachDetailScreen } from './BeachDetailScreen';
import { Beach } from '../types/beach';
import { BeachConditions, useBeachForecastSeries } from '../hooks/useBeachForecastSeries';
import { useUserLocation } from '../hooks/useUserLocation';
import { useBeachDistances } from '../hooks/useBeachDistances';
import { useLocale } from '../i18n/LocaleContext';
import { useCommunityBeaches } from '../context/CommunityBeachesContext';
import { useFavorites } from '../context/FavoritesContext';
import { Prefecture } from '../types/beach';
import { DISTANCE_FILTER_MINUTES, DistanceFilter, SortOption } from '../types/filters';
import { windLevel } from '../utils/wind';
import { formatDayLabel, pickConditionsForOffset } from '../utils/forecastSelect';
import { normalizeForSearch } from '../utils/transliteration';

interface ConditionsState {
  loading: boolean;
  error: boolean;
  conditions: BeachConditions | null;
}

export function BeachListScreen({ dayOffset }: { dayOffset: number }) {
  const { locale, strings } = useLocale();
  const { beaches: communityBeaches, refresh: refreshCommunity } = useCommunityBeaches();
  const { favorites } = useFavorites();
  const allBeaches = useMemo(() => [...BEACHES, ...communityBeaches], [communityBeaches]);

  const { series: seriesMap, refresh: refreshSeries, refreshing } = useBeachForecastSeries(allBeaches);
  const loadedCount = useMemo(
    () => allBeaches.filter((b) => seriesMap[b.id] && !seriesMap[b.id].loading).length,
    [allBeaches, seriesMap]
  );
  const stillLoadingInitial = loadedCount < allBeaches.length;
  const { status: locationStatus, coords, requestLocation } = useUserLocation();
  const { distances } = useBeachDistances(coords, allBeaches);

  const [search, setSearch] = useState('');
  const [prefecture, setPrefecture] = useState<Prefecture | 'all'>('all');
  const [calmOnly, setCalmOnly] = useState(false);
  const [favoritesOnly, setFavoritesOnly] = useState(false);
  const [distanceFilter, setDistanceFilter] = useState<DistanceFilter>('all');
  const [sortBy, setSortBy] = useState<SortOption>('conditions');
  const [selectedBeach, setSelectedBeach] = useState<Beach | null>(null);

  const conditionsMap = useMemo(() => {
    const map: Record<string, ConditionsState> = {};
    allBeaches.forEach((beach) => {
      const entry = seriesMap[beach.id];
      map[beach.id] = {
        loading: entry?.loading ?? true,
        error: entry?.error ?? false,
        conditions: entry?.series ? pickConditionsForOffset(entry.series, dayOffset) : null,
      };
    });
    return map;
  }, [allBeaches, seriesMap, dayOffset]);

  const refresh = () => {
    refreshSeries();
    refreshCommunity();
  };

  const filteredBeaches = useMemo(() => {
    const query = normalizeForSearch(search);

    return allBeaches.filter((beach) => {
      if (prefecture !== 'all' && beach.prefecture !== prefecture) return false;

      if (query) {
        // Transliteration-normalized, so searching in Greek finds beaches
        // only ever tagged with a Latin name in OpenStreetMap, and vice versa.
        const matches =
          normalizeForSearch(beach.nameEl).includes(query) || normalizeForSearch(beach.nameEn).includes(query);
        if (!matches) return false;
      }

      if (calmOnly) {
        const conditions = conditionsMap[beach.id]?.conditions;
        if (!conditions || windLevel(conditions.windSpeedKmh).key !== 'calm') return false;
      }

      if (favoritesOnly && !favorites.has(beach.id)) return false;

      if (distanceFilter !== 'all' && coords) {
        const distance = distances[beach.id];
        const minutes =
          distance?.drivingMinutes ?? (distance ? (distance.straightLineKm / 45) * 60 : null);
        if (minutes === null || minutes > DISTANCE_FILTER_MINUTES[distanceFilter]) return false;
      }

      return true;
    });
  }, [allBeaches, search, prefecture, calmOnly, favoritesOnly, favorites, distanceFilter, coords, conditionsMap, distances]);

  const sortedBeaches = useMemo(() => {
    if (sortBy === 'alphabetical') {
      const name = (b: Beach) => (locale === 'el' ? b.nameEl : b.nameEn);
      return [...filteredBeaches].sort((a, b) => name(a).localeCompare(name(b), locale));
    }

    if (sortBy === 'distance' && coords) {
      return [...filteredBeaches].sort((a, b) => {
        const da = distances[a.id]?.drivingKm ?? distances[a.id]?.straightLineKm ?? null;
        const db = distances[b.id]?.drivingKm ?? distances[b.id]?.straightLineKm ?? null;
        if (da !== null && db !== null) return da - db;
        if (da !== null) return -1;
        if (db !== null) return 1;
        return 0;
      });
    }

    if (sortBy === 'temperature') {
      return [...filteredBeaches].sort((a, b) => {
        const ta = conditionsMap[a.id]?.conditions?.temperatureC;
        const tb = conditionsMap[b.id]?.conditions?.temperatureC;
        if (ta !== undefined && tb !== undefined) return tb - ta;
        if (ta !== undefined) return -1;
        if (tb !== undefined) return 1;
        return 0;
      });
    }

    // Default: best conditions first (calmest wind).
    return [...filteredBeaches].sort((a, b) => {
      const ca = conditionsMap[a.id]?.conditions;
      const cb = conditionsMap[b.id]?.conditions;
      if (ca && cb) return ca.windSpeedKmh - cb.windSpeedKmh;
      if (ca) return -1;
      if (cb) return 1;
      return 0;
    });
  }, [filteredBeaches, conditionsMap, sortBy, locale, coords, distances]);

  // Independent of how the list is currently sorted for display — the
  // "best pick" badge always reflects the calmest conditions.
  const topPick = useMemo(() => {
    return [...filteredBeaches]
      .filter((b) => conditionsMap[b.id]?.conditions)
      .sort((a, b) => conditionsMap[a.id]!.conditions!.windSpeedKmh - conditionsMap[b.id]!.conditions!.windSpeedKmh)[0];
  }, [filteredBeaches, conditionsMap]);
  const dayLabel = formatDayLabel(dayOffset, locale, strings.dateSelector.today, strings.dateSelector.tomorrow);

  const clearFilters = () => {
    setSearch('');
    setPrefecture('all');
    setCalmOnly(false);
    setFavoritesOnly(false);
    setDistanceFilter('all');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={sortedBeaches}
        keyExtractor={(beach) => beach.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={refresh} />}
        renderItem={({ item }) => (
          <BeachCard
            beach={item}
            state={conditionsMap[item.id] ?? { loading: true, error: false, conditions: null }}
            distance={coords ? distances[item.id] : null}
            isTopPick={item.id === topPick?.id}
            dayLabel={dayLabel}
            onPress={() => setSelectedBeach(item)}
          />
        )}
        ListHeaderComponent={
          <View>
            <View style={styles.headerContainer}>
              <Text style={styles.title}>🌊 {strings.appTitle}</Text>
              <Text style={styles.subtitle}>{strings.appSubtitle}</Text>
            </View>

            <TextInput
              style={styles.searchInput}
              placeholder={strings.filters.searchPlaceholder}
              placeholderTextColor="#8ba3b0"
              value={search}
              onChangeText={setSearch}
            />

            <SortSelector sortBy={sortBy} onChange={setSortBy} distanceAvailable={locationStatus === 'granted'} />

            {stillLoadingInitial && (
              <View style={styles.progressBanner}>
                <ActivityIndicator size="small" color="#0b6e99" />
                <Text style={styles.progressText}>
                  {strings.status.loadingProgress} ({loadedCount}/{allBeaches.length})
                </Text>
              </View>
            )}

            <LocationPrompt status={locationStatus} onRequest={requestLocation} />

            <FilterBar
              prefecture={prefecture}
              onPrefectureChange={setPrefecture}
              calmOnly={calmOnly}
              onCalmOnlyChange={setCalmOnly}
              favoritesOnly={favoritesOnly}
              onFavoritesOnlyChange={setFavoritesOnly}
              distanceFilter={distanceFilter}
              onDistanceFilterChange={setDistanceFilter}
              distanceAvailable={locationStatus === 'granted'}
            />
          </View>
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>{strings.empty}</Text>
            <Pressable style={styles.emptyButton} onPress={clearFilters}>
              <Text style={styles.emptyButtonText}>{strings.clearFilters}</Text>
            </Pressable>
          </View>
        }
        contentContainerStyle={styles.listContent}
      />

      <BeachDetailScreen
        beach={selectedBeach}
        distance={selectedBeach && coords ? distances[selectedBeach.id] : null}
        dayOffset={dayOffset}
        onClose={() => setSelectedBeach(null)}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#eef7fb',
  },
  listContent: {
    paddingBottom: 24,
    flexGrow: 1,
  },
  headerContainer: {
    paddingTop: 16,
    paddingHorizontal: 16,
    paddingBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#0b6e99',
  },
  searchInput: {
    marginHorizontal: 16,
    marginBottom: 12,
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 10,
    fontSize: 14,
    color: '#123',
  },
  subtitle: {
    fontSize: 14,
    color: '#33586b',
    marginTop: 4,
  },
  progressBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 10,
    borderRadius: 10,
    backgroundColor: '#dcebf2',
  },
  progressText: {
    fontSize: 12,
    color: '#33586b',
    flexShrink: 1,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 24,
  },
  emptyText: {
    fontSize: 15,
    color: '#678',
    textAlign: 'center',
    marginBottom: 12,
  },
  emptyButton: {
    backgroundColor: '#0b6e99',
    paddingVertical: 10,
    paddingHorizontal: 18,
    borderRadius: 12,
  },
  emptyButtonText: {
    color: '#fff',
    fontWeight: '700',
  },
});
