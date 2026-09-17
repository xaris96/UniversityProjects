import { ScrollView, StyleSheet } from 'react-native';
import { useLocale } from '../i18n/LocaleContext';
import { SortOption } from '../types/filters';
import { Chip } from './Chip';

export function SortSelector({
  sortBy,
  onChange,
  distanceAvailable,
}: {
  sortBy: SortOption;
  onChange: (value: SortOption) => void;
  distanceAvailable: boolean;
}) {
  const { strings } = useLocale();

  const options: SortOption[] = distanceAvailable
    ? ['conditions', 'distance', 'alphabetical', 'temperature']
    : ['conditions', 'alphabetical', 'temperature'];

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.scrollView}
      contentContainerStyle={styles.row}
    >
      {options.map((option) => (
        <Chip
          key={option}
          label={strings.sort[option]}
          active={sortBy === option}
          onPress={() => onChange(option)}
        />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flexGrow: 0,
    flexShrink: 0,
    height: 36,
    marginBottom: 12,
  },
  row: {
    paddingHorizontal: 16,
    gap: 8,
    alignItems: 'flex-start',
  },
});
