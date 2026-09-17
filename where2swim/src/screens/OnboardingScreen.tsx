import { useEffect, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Modal, Pressable, StyleSheet, Text, View } from 'react-native';
import { useLocale } from '../i18n/LocaleContext';

const STORAGE_KEY = 'where2swim.onboarding_seen';

export function useOnboarding() {
  const [visible, setVisible] = useState(false);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const seen = await AsyncStorage.getItem(STORAGE_KEY);
        if (!seen) setVisible(true);
      } catch {
        // Storage unavailable — just skip onboarding rather than blocking.
      } finally {
        setChecked(true);
      }
    })();
  }, []);

  const dismiss = () => {
    setVisible(false);
    AsyncStorage.setItem(STORAGE_KEY, '1').catch(() => {});
  };

  return { visible: checked && visible, dismiss };
}

export function OnboardingScreen({ visible, onDismiss }: { visible: boolean; onDismiss: () => void }) {
  const { strings } = useLocale();

  return (
    <Modal visible={visible} animationType="fade" transparent onRequestClose={onDismiss}>
      <View style={styles.backdrop}>
        <View style={styles.card}>
          <Text style={styles.title}>{strings.onboarding.title}</Text>
          <Text style={styles.body}>{strings.onboarding.body}</Text>
          <Pressable style={styles.button} onPress={onDismiss}>
            <Text style={styles.buttonText}>{strings.onboarding.cta}</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(11,110,153,0.9)',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    width: '100%',
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    color: '#0b6e99',
    marginBottom: 12,
  },
  body: {
    fontSize: 15,
    color: '#345',
    lineHeight: 22,
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#0b6e99',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 15,
  },
});
