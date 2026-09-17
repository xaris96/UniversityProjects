import { ScrollView, StyleSheet } from 'react-native';
import { useLocale } from '../i18n/LocaleContext';
import { formatDayLabel } from '../utils/forecastSelect';
import { Chip } from './Chip';

const DAY_OFFSETS = [0, 1, 2, 3, 4];

export function DateSelector({ dayOffset, onChange }: { dayOffset: number; onChange: (offset: number) => void }) {
  const { locale, strings } = useLocale();

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.scrollView}
      contentContainerStyle={styles.row}
    >
      {DAY_OFFSETS.map((offset) => (
        <Chip
          key={offset}
          label={formatDayLabel(offset, locale, strings.dateSelector.today, strings.dateSelector.tomorrow)}
          active={dayOffset === offset}
          onPress={() => onChange(offset)}
        />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flexGrow: 0,
    flexShrink: 0,
    height: 44,
  },
  row: {
    paddingHorizontal: 16,
    paddingBottom: 12,
    gap: 8,
    alignItems: 'flex-start',
  },
});
