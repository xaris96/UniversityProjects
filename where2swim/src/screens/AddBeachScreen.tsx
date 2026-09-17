import { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import MapView, { Marker, MapPressEvent } from 'react-native-maps';
import { Ionicons } from '@expo/vector-icons';
import { useLocale } from '../i18n/LocaleContext';
import { useCommunityBeaches } from '../context/CommunityBeachesContext';
import { Coast, Prefecture } from '../types/beach';
import { Chip } from '../components/Chip';
import { BEACHES } from '../data/beaches';
import { searchCreteLocations, GeocodeResult } from '../utils/geocoding';
import { inferPrefectureFromLongitude } from '../utils/prefecture';
import { inferCoastFromCoordinates } from '../utils/coast';
import { findPossibleDuplicate } from '../utils/duplicates';
import { normalizeForSearch } from '../utils/transliteration';
import { isSupabaseConfigured, supabase } from '../lib/supabase';
import { ensureAnonymousUser } from '../lib/auth';

const CRETE_REGION = {
  latitude: 35.24,
  longitude: 24.8,
  latitudeDelta: 1.3,
  longitudeDelta: 3.3,
};

const PREFECTURES: Prefecture[] = ['chania', 'rethymno', 'heraklion', 'lasithi'];
const COASTS: Coast[] = ['N', 'S', 'E', 'W'];

type SubmitState = 'idle' | 'submitting' | 'success' | 'error';

export function AddBeachScreen({ visible, onClose }: { visible: boolean; onClose: () => void }) {
  const { locale, strings } = useLocale();
  const { beaches: communityBeaches, addBeach, refresh } = useCommunityBeaches();

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<GeocodeResult[]>([]);
  const [searching, setSearching] = useState(false);

  const [coords, setCoords] = useState<{ latitude: number; longitude: number } | null>(null);
  const [name, setName] = useState('');
  const [nameLocked, setNameLocked] = useState(false);
  const [prefecture, setPrefecture] = useState<Prefecture | null>(null);
  const [coast, setCoast] = useState<Coast | null>(null);

  const [submitState, setSubmitState] = useState<SubmitState>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  // Instant, offline check against beaches already in the app (built-in +
  // approved community ones) — no need to wait on any network call to
  // notice "this already exists" while typing.
  const existingMatches = useMemo(() => {
    const query = normalizeForSearch(searchQuery);
    if (query.length < 2) return [];
    const all = [...BEACHES, ...communityBeaches];
    return all
      .filter((b) => normalizeForSearch(b.nameEl).includes(query) || normalizeForSearch(b.nameEn).includes(query))
      .slice(0, 4);
  }, [searchQuery, communityBeaches]);

  function resetForm() {
    setSearchQuery('');
    setSearchResults([]);
    setCoords(null);
    setName('');
    setNameLocked(false);
    setPrefecture(null);
    setCoast(null);
    setSubmitState('idle');
    setErrorMessage('');
  }

  function handleClose() {
    resetForm();
    onClose();
  }

  function setLocation(latitude: number, longitude: number) {
    setCoords({ latitude, longitude });
    setPrefecture(inferPrefectureFromLongitude(longitude));
    setCoast(inferCoastFromCoordinates(latitude, longitude));
  }

  useEffect(() => {
    const query = searchQuery.trim();
    if (query.length < 2) {
      setSearchResults([]);
      setSearching(false);
      return;
    }

    let cancelled = false;
    setSearching(true);
    const debounce = setTimeout(async () => {
      try {
        const results = await searchCreteLocations(query);
        if (!cancelled) setSearchResults(results);
      } catch {
        if (!cancelled) setSearchResults([]);
      } finally {
        if (!cancelled) setSearching(false);
      }
    }, 350);

    return () => {
      cancelled = true;
      clearTimeout(debounce);
    };
  }, [searchQuery]);

  async function handleRetrySearch() {
    const query = searchQuery.trim();
    if (query.length < 2) return;
    setSearching(true);
    try {
      const results = await searchCreteLocations(query);
      setSearchResults(results);
    } catch {
      setSearchResults([]);
    } finally {
      setSearching(false);
    }
  }

  function handlePickResult(result: GeocodeResult) {
    setLocation(result.latitude, result.longitude);
    setSearchResults([]);
    setSearchQuery('');
    setName(result.name);
    setNameLocked(true);
  }

  function handleMapPress(event: MapPressEvent) {
    const { latitude, longitude } = event.nativeEvent.coordinate;
    setLocation(latitude, longitude);
    setNameLocked(false);
  }

  function handleMarkerDragEnd(latitude: number, longitude: number) {
    // Just fine-tuning the pin — keep whatever name/lock state we had
    // (e.g. still locked if this location came from a search result).
    setCoords({ latitude, longitude });
    setPrefecture(inferPrefectureFromLongitude(longitude));
    setCoast(inferCoastFromCoordinates(latitude, longitude));
  }

  async function performSubmit() {
    if (!name.trim() || !coords || !coast || !prefecture || !supabase) return;

    setSubmitState('submitting');

    await ensureAnonymousUser();
    const { data: userData } = await supabase.auth.getUser();
    const submittedBy = userData.user?.id;
    if (!submittedBy) {
      setSubmitState('error');
      setErrorMessage(strings.addBeach.errorGeneric);
      return;
    }

    const { data, error } = await supabase
      .from('community_beaches')
      .insert({
        name: name.trim(),
        prefecture,
        coast,
        latitude: coords.latitude,
        longitude: coords.longitude,
        submitted_by: submittedBy,
      })
      .select()
      .single();

    if (error || !data) {
      setSubmitState('error');
      setErrorMessage(strings.addBeach.errorGeneric);
      return;
    }

    addBeach({
      id: `community-${data.id}`,
      nameEl: data.name,
      nameEn: data.name,
      prefecture: data.prefecture,
      coast: data.coast,
      latitude: data.latitude,
      longitude: data.longitude,
      source: 'community',
      status: data.status,
    });
    refresh();
    setSubmitState('success');
  }

  function handleSubmit() {
    if (!name.trim() || !coords || !coast || !prefecture) {
      setSubmitState('error');
      setErrorMessage(strings.addBeach.errorIncomplete);
      return;
    }
    if (!supabase) {
      setSubmitState('error');
      setErrorMessage(strings.addBeach.notConfigured);
      return;
    }

    const existingBeaches = [...BEACHES, ...communityBeaches];
    const duplicate = findPossibleDuplicate(
      { name: name.trim(), latitude: coords.latitude, longitude: coords.longitude },
      existingBeaches
    );

    if (duplicate) {
      const duplicateName = locale === 'el' ? duplicate.nameEl : duplicate.nameEn;
      Alert.alert(strings.addBeach.duplicateTitle, `${strings.addBeach.duplicateMessage} "${duplicateName}".`, [
        { text: strings.addBeach.duplicateCancel, style: 'cancel' },
        { text: strings.addBeach.duplicateConfirm, style: 'destructive', onPress: () => performSubmit() },
      ]);
      return;
    }

    performSubmit();
  }

  return (
    <Modal visible={visible} animationType="slide" onRequestClose={handleClose}>
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
          <View style={styles.headerRow}>
            <Text style={styles.title}>{strings.addBeach.title}</Text>
            <Pressable onPress={handleClose}>
              <Text style={styles.closeText}>✕</Text>
            </Pressable>
          </View>

          {!isSupabaseConfigured && <Text style={styles.notConfiguredText}>{strings.addBeach.notConfigured}</Text>}

          {submitState === 'success' ? (
            <View style={styles.successBox}>
              <Text style={styles.successText}>{strings.addBeach.success}</Text>
              <Pressable style={styles.submitButton} onPress={handleClose}>
                <Text style={styles.submitButtonText}>{strings.addBeach.close}</Text>
              </Pressable>
            </View>
          ) : (
            <>
              <Text style={styles.label}>{strings.addBeach.searchLabel}</Text>
              <View style={styles.searchRow}>
                <TextInput
                  style={styles.searchInput}
                  placeholder={strings.addBeach.searchPlaceholder}
                  placeholderTextColor="#8ba3b0"
                  value={searchQuery}
                  onChangeText={setSearchQuery}
                />
                {searching && <ActivityIndicator style={styles.searchSpinner} color="#0b6e99" size="small" />}
              </View>

              {existingMatches.length > 0 && (
                <View style={styles.existingBox}>
                  <Text style={styles.existingTitle}>{strings.addBeach.alreadyInAppSection}</Text>
                  {existingMatches.map((b) => (
                    <Text key={b.id} style={styles.existingItem}>
                      ✅ {locale === 'el' ? b.nameEl : b.nameEn} — {strings.prefectures[b.prefecture]}
                    </Text>
                  ))}
                </View>
              )}

              {searchResults.map((result, index) => {
                const showNearbyHeader = result.isNearby && (index === 0 || !searchResults[index - 1].isNearby);
                return (
                  <View key={`${result.latitude}-${result.longitude}-${index}`}>
                    {showNearbyHeader && <Text style={styles.resultSectionLabel}>{strings.addBeach.nearbySection}</Text>}
                    <Pressable style={styles.resultRow} onPress={() => handlePickResult(result)}>
                      <Text style={styles.resultText} numberOfLines={2}>
                        {result.label}
                      </Text>
                    </Pressable>
                  </View>
                );
              })}

              {!searching && searchQuery.trim().length >= 2 && searchResults.length === 0 && (
                <View>
                  <Text style={styles.hintText}>{strings.addBeach.searchNoResults}</Text>
                  <Pressable style={styles.retryButton} onPress={handleRetrySearch}>
                    <Ionicons name="refresh-outline" size={14} color="#0b6e99" />
                    <Text style={styles.retryButtonText}>{strings.addBeach.retrySearch}</Text>
                  </Pressable>
                </View>
              )}

              <Text style={styles.label}>{strings.addBeach.mapLabel}</Text>
              <MapView
                style={styles.map}
                initialRegion={CRETE_REGION}
                region={coords ? { ...coords, latitudeDelta: 0.15, longitudeDelta: 0.15 } : undefined}
                onPress={handleMapPress}
              >
                {coords && (
                  <Marker
                    coordinate={coords}
                    draggable
                    onDragEnd={(e) =>
                      handleMarkerDragEnd(e.nativeEvent.coordinate.latitude, e.nativeEvent.coordinate.longitude)
                    }
                  />
                )}
              </MapView>
              <Text style={styles.hintText}>
                {coords ? strings.addBeach.mapHintHasLocation : strings.addBeach.mapHintNoLocation}
              </Text>

              <Text style={styles.label}>{strings.addBeach.nameLabel}</Text>
              <View style={styles.nameRow}>
                <TextInput
                  style={[styles.nameInput, nameLocked && styles.nameInputLocked]}
                  placeholder={strings.addBeach.namePlaceholder}
                  placeholderTextColor="#8ba3b0"
                  value={name}
                  onChangeText={setName}
                  editable={!nameLocked}
                />
                {nameLocked && (
                  <Pressable style={styles.unlockButton} onPress={() => setNameLocked(false)} hitSlop={8}>
                    <Ionicons name="pencil-outline" size={16} color="#0b6e99" />
                  </Pressable>
                )}
              </View>
              {nameLocked && <Text style={styles.hintText}>{strings.addBeach.nameLockedHint}</Text>}

              <Text style={styles.label}>{strings.addBeach.prefectureLabel}</Text>
              <View style={styles.chipRow}>
                {PREFECTURES.map((p) => (
                  <Chip key={p} label={strings.prefectures[p]} active={prefecture === p} onPress={() => setPrefecture(p)} />
                ))}
              </View>

              <Text style={styles.label}>{strings.addBeach.coastLabel}</Text>
              <View style={styles.chipRow}>
                {COASTS.map((c) => (
                  <Chip key={c} label={strings.coasts[c]} active={coast === c} onPress={() => setCoast(c)} />
                ))}
              </View>

              {submitState === 'error' && <Text style={styles.errorText}>{errorMessage}</Text>}

              <Pressable
                style={[styles.submitButton, submitState === 'submitting' && styles.submitButtonDisabled]}
                onPress={handleSubmit}
                disabled={submitState === 'submitting'}
              >
                {submitState === 'submitting' ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <Text style={styles.submitButtonText}>{strings.addBeach.submit}</Text>
                )}
              </Pressable>
            </>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  flex: {
    flex: 1,
  },
  container: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#eef7fb',
    flexGrow: 1,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    color: '#0b6e99',
  },
  closeText: {
    fontSize: 22,
    color: '#33586b',
  },
  notConfiguredText: {
    fontSize: 13,
    color: '#c62828',
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#33586b',
    marginTop: 16,
    marginBottom: 8,
  },
  searchRow: {
    justifyContent: 'center',
  },
  searchInput: {
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 10,
    paddingRight: 36,
    fontSize: 14,
    color: '#123',
  },
  searchSpinner: {
    position: 'absolute',
    right: 12,
  },
  retryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    alignSelf: 'flex-start',
    marginTop: 8,
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 16,
    backgroundColor: '#dcebf2',
  },
  retryButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#0b6e99',
  },
  existingBox: {
    backgroundColor: '#e8f5e9',
    borderRadius: 10,
    padding: 10,
    marginTop: 6,
    gap: 4,
  },
  existingTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: '#2e7d32',
  },
  existingItem: {
    fontSize: 13,
    color: '#2e7d32',
  },
  resultSectionLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#678',
    marginTop: 10,
    marginBottom: 2,
  },
  resultRow: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 10,
    marginTop: 6,
  },
  resultText: {
    fontSize: 13,
    color: '#345',
  },
  map: {
    height: 220,
    borderRadius: 12,
  },
  hintText: {
    fontSize: 12,
    color: '#678',
    marginTop: 6,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  nameInput: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 10,
    fontSize: 14,
    color: '#123',
  },
  nameInputLocked: {
    color: '#345',
    backgroundColor: '#eef4f7',
  },
  unlockButton: {
    padding: 8,
  },
  chipRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  errorText: {
    fontSize: 13,
    color: '#c62828',
    marginTop: 16,
  },
  submitButton: {
    backgroundColor: '#0b6e99',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonDisabled: {
    opacity: 0.7,
  },
  submitButtonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 15,
  },
  successBox: {
    alignItems: 'center',
    paddingTop: 40,
  },
  successText: {
    fontSize: 16,
    color: '#2e7d32',
    textAlign: 'center',
    marginBottom: 20,
  },
});
