import { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { Pressable, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { BeachListScreen } from './src/screens/BeachListScreen';
import { MapScreen } from './src/screens/MapScreen';
import { AddBeachScreen } from './src/screens/AddBeachScreen';
import { OnboardingScreen, useOnboarding } from './src/screens/OnboardingScreen';
import { LanguageToggle } from './src/components/LanguageToggle';
import { DateSelector } from './src/components/DateSelector';
import { LocaleProvider, useLocale } from './src/i18n/LocaleContext';
import { CommunityBeachesProvider } from './src/context/CommunityBeachesContext';
import { FavoritesProvider } from './src/context/FavoritesContext';

type Tab = 'list' | 'map';

function AppContent() {
  const [tab, setTab] = useState<Tab>('list');
  const [addBeachOpen, setAddBeachOpen] = useState(false);
  const [dayOffset, setDayOffset] = useState(0);
  const { strings } = useLocale();
  const onboarding = useOnboarding();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.tabBar}>
        <View style={styles.tabGroup}>
          <Pressable
            style={[styles.tabButton, tab === 'list' && styles.tabButtonActive]}
            onPress={() => setTab('list')}
          >
            <Text style={[styles.tabLabel, tab === 'list' && styles.tabLabelActive]}>{strings.tabs.list}</Text>
          </Pressable>
          <Pressable
            style={[styles.tabButton, tab === 'map' && styles.tabButtonActive]}
            onPress={() => setTab('map')}
          >
            <Text style={[styles.tabLabel, tab === 'map' && styles.tabLabelActive]}>{strings.tabs.map}</Text>
          </Pressable>
        </View>
        <LanguageToggle />
      </View>

      <DateSelector dayOffset={dayOffset} onChange={setDayOffset} />

      {tab === 'list' ? <BeachListScreen dayOffset={dayOffset} /> : <MapScreen dayOffset={dayOffset} />}

      <Pressable style={styles.fab} onPress={() => setAddBeachOpen(true)}>
        <Text style={styles.fabText}>+</Text>
      </Pressable>

      <AddBeachScreen visible={addBeachOpen} onClose={() => setAddBeachOpen(false)} />

      <OnboardingScreen visible={onboarding.visible} onDismiss={onboarding.dismiss} />

      <StatusBar style="dark" />
    </SafeAreaView>
  );
}

export default function App() {
  return (
    <LocaleProvider>
      <FavoritesProvider>
        <CommunityBeachesProvider>
          <AppContent />
        </CommunityBeachesProvider>
      </FavoritesProvider>
    </LocaleProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#eef7fb',
  },
  tabBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 8,
    paddingBottom: 12,
  },
  tabGroup: {
    flexDirection: 'row',
    gap: 8,
  },
  tabButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    backgroundColor: '#dcebf2',
  },
  tabButtonActive: {
    backgroundColor: '#0b6e99',
  },
  tabLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#33586b',
  },
  tabLabelActive: {
    color: '#fff',
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 28,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#0b6e99',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
    elevation: 4,
  },
  fabText: {
    color: '#fff',
    fontSize: 30,
    fontWeight: '400',
    marginTop: -2,
  },
});
