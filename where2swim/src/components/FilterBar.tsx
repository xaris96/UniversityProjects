import { useState } from 'react';
import { LayoutAnimation, Platform, Pressable, ScrollView, StyleSheet, Text, UIManager, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocale } from '../i18n/LocaleContext';
import { Prefecture } from '../types/beach';
import { DistanceFilter } from '../types/filters';
import { Chip } from './Chip';

if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

interface FilterBarProps {
  prefecture: Prefecture | 'all';
  onPrefectureChange: (value: Prefecture | 'all') => void;
  calmOnly: boolean;
  onCalmOnlyChange: (value: boolean) => void;
  favoritesOnly: boolean;
  onFavoritesOnlyChange: (value: boolean) => void;
  distanceFilter: DistanceFilter;
  onDistanceFilterChange: (value: DistanceFilter) => void;
  distanceAvailable: boolean;
}

const PREFECTURES: (Prefecture | 'all')[] = ['all', 'chania', 'rethymno', 'heraklion', 'lasithi'];
const DISTANCE_OPTIONS: DistanceFilter[] = ['all', 'within30', 'within1h', 'within2h'];

export function FilterBar({
  prefecture,
  onPrefectureChange,
  calmOnly,
  onCalmOnlyChange,
  favoritesOnly,
  onFavoritesOnlyChange,
  distanceFilter,
  onDistanceFilterChange,
  distanceAvailable,
}: FilterBarProps) {
  const { strings } = useLocale();
  const [expanded, setExpanded] = useState(false);

  const activeCount =
    (prefecture !== 'all' ? 1 : 0) +
    (calmOnly ? 1 : 0) +
    (favoritesOnly ? 1 : 0) +
    (distanceAvailable && distanceFilter !== 'all' ? 1 : 0);

  const distanceLabel = (option: DistanceFilter) => {
    switch (option) {
      case 'all':
        return strings.filters.distanceAll;
      case 'within30':
        return strings.filters.distanceWithin30;
      case 'within1h':
        return strings.filters.distanceWithin1h;
      case 'within2h':
        return strings.filters.distanceWithin2h;
    }
  };

  const toggleExpanded = () => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpanded((e) => !e);
  };

  return (
    <View style={styles.container}>
      <Pressable style={styles.toggleButton} onPress={toggleExpanded}>
        <Ionicons name="options-outline" size={18} color="#0b6e99" />
        <Text style={styles.toggleLabel}>{strings.filters.title}</Text>
        {activeCount > 0 && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{activeCount}</Text>
          </View>
        )}
        <Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={16} color="#33586b" />
      </Pressable>

      {expanded && (
        <View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
            {PREFECTURES.map((p) => (
              <Chip
                key={p}
                label={p === 'all' ? strings.prefectures.all : strings.prefectures[p]}
                active={prefecture === p}
                onPress={() => onPrefectureChange(p)}
              />
            ))}
          </ScrollView>

          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
            <Chip label={strings.filters.conditionAll} active={!calmOnly} onPress={() => onCalmOnlyChange(false)} />
            <Chip
              label={strings.filters.conditionCalmOnly}
              active={calmOnly}
              onPress={() => onCalmOnlyChange(true)}
            />
          </ScrollView>

          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
            <Chip
              label={strings.filters.favoritesAll}
              active={!favoritesOnly}
              onPress={() => onFavoritesOnlyChange(false)}
            />
            <Chip
              label={strings.filters.favoritesOnly}
              active={favoritesOnly}
              onPress={() => onFavoritesOnlyChange(true)}
            />
          </ScrollView>

          {distanceAvailable && (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
              {DISTANCE_OPTIONS.map((option) => (
                <Chip
                  key={option}
                  label={distanceLabel(option)}
                  active={distanceFilter === option}
                  onPress={() => onDistanceFilterChange(option)}
                />
              ))}
            </ScrollView>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 4,
  },
  toggleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: 6,
    marginHorizontal: 16,
    marginBottom: 8,
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    backgroundColor: '#fff',
  },
  toggleLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#0b6e99',
  },
  badge: {
    backgroundColor: '#0b6e99',
    borderRadius: 10,
    minWidth: 18,
    height: 18,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 4,
  },
  badgeText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: '700',
  },
  chipRow: {
    paddingHorizontal: 16,
    paddingBottom: 8,
    gap: 8,
    alignItems: 'flex-start',
  },
});
