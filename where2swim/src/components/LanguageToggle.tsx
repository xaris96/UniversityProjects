import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useLocale } from '../i18n/LocaleContext';
import { Locale } from '../i18n/translations';

export function LanguageToggle() {
  const { locale, setLocale } = useLocale();

  const renderOption = (value: Locale, label: string) => (
    <Pressable
      key={value}
      style={[styles.option, locale === value && styles.optionActive]}
      onPress={() => setLocale(value)}
    >
      <Text style={[styles.optionText, locale === value && styles.optionTextActive]}>{label}</Text>
    </Pressable>
  );

  return (
    <View style={styles.container}>
      {renderOption('el', 'EL')}
      {renderOption('en', 'EN')}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#dcebf2',
    borderRadius: 16,
    padding: 2,
  },
  option: {
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 14,
  },
  optionActive: {
    backgroundColor: '#0b6e99',
  },
  optionText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#33586b',
  },
  optionTextActive: {
    color: '#fff',
  },
});
