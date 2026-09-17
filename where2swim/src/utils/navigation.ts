import { Linking, Platform, Share } from 'react-native';
import { Beach } from '../types/beach';
import { Locale } from '../i18n/translations';

export async function openDirections(beach: Beach): Promise<void> {
  const { latitude, longitude } = beach;
  const webFallback = `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;

  const nativeUrl = Platform.select({
    ios: `maps://app?daddr=${latitude},${longitude}&dirflg=d`,
    android: `google.navigation:q=${latitude},${longitude}`,
    default: webFallback,
  });

  try {
    const canOpen = await Linking.canOpenURL(nativeUrl);
    await Linking.openURL(canOpen ? nativeUrl : webFallback);
  } catch {
    await Linking.openURL(webFallback);
  }
}

export async function shareBeach(beach: Beach, locale: Locale): Promise<void> {
  const name = locale === 'el' ? beach.nameEl : beach.nameEn;
  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${beach.latitude},${beach.longitude}`;
  const message =
    locale === 'el'
      ? `🌊 ${name} — δες τις live συνθήκες ανέμου/κύματος στο Where2Swim!\n${mapsUrl}`
      : `🌊 ${name} — check live wind/wave conditions on Where2Swim!\n${mapsUrl}`;

  try {
    await Share.share({ message });
  } catch {
    // user cancelled or share sheet unavailable — nothing to do
  }
}
