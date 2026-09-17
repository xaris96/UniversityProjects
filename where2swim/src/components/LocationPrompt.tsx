import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { useLocale } from '../i18n/LocaleContext';
import { LocationStatus } from '../hooks/useUserLocation';

export function LocationPrompt({ status, onRequest }: { status: LocationStatus; onRequest: () => void }) {
  const { strings } = useLocale();

  if (status === 'granted') return null;

  return (
    <View style={styles.container}>
      {status === 'requesting' ? (
        <View style={styles.row}>
          <ActivityIndicator />
          <Text style={styles.text}>{strings.location.requesting}</Text>
        </View>
      ) : status === 'denied' ? (
        <Text style={styles.deniedText}>{strings.location.denied}</Text>
      ) : (
        <View style={styles.row}>
          <Text style={styles.text}>{strings.location.prompt}</Text>
          <Pressable style={styles.button} onPress={onRequest}>
            <Text style={styles.buttonText}>{strings.location.enable}</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 12,
    borderRadius: 12,
    backgroundColor: '#fff8e1',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 8,
  },
  text: {
    flex: 1,
    fontSize: 13,
    color: '#5d4a00',
  },
  deniedText: {
    fontSize: 13,
    color: '#8a4b00',
  },
  button: {
    backgroundColor: '#0b6e99',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 13,
    fontWeight: '700',
  },
});
