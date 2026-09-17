import { Pressable, StyleSheet, Text } from 'react-native';

export function Chip({ label, active, onPress }: { label: string; active: boolean; onPress: () => void }) {
  return (
    <Pressable style={[styles.chip, active && styles.chipActive]} onPress={onPress}>
      <Text style={[styles.chipText, active && styles.chipTextActive]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  chip: {
    paddingVertical: 6,
    paddingHorizontal: 14,
    borderRadius: 16,
    backgroundColor: '#dcebf2',
  },
  chipActive: {
    backgroundColor: '#0b6e99',
  },
  chipText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#33586b',
  },
  chipTextActive: {
    color: '#fff',
  },
});
