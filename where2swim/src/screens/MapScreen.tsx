import { useMemo } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import MapView, { Callout, Marker } from 'react-native-maps';
import { BEACHES } from '../data/beaches';
import { useBeachForecastSeries } from '../hooks/useBeachForecastSeries';
import { degreesToCompass, windLevel } from '../utils/wind';
import { pickConditionsForOffset } from '../utils/forecastSelect';
import { useLocale } from '../i18n/LocaleContext';
import { useCommunityBeaches } from '../context/CommunityBeachesContext';

const CRETE_REGION = {
  latitude: 35.24,
  longitude: 24.8,
  latitudeDelta: 1.3,
  longitudeDelta: 3.3,
};

export function MapScreen({ dayOffset }: { dayOffset: number }) {
  const { locale, strings } = useLocale();
  const { beaches: communityBeaches } = useCommunityBeaches();
  const allBeaches = useMemo(() => [...BEACHES, ...communityBeaches], [communityBeaches]);
  const { series: seriesMap } = useBeachForecastSeries(allBeaches);

  return (
    <View style={styles.container}>
      <MapView style={styles.map} initialRegion={CRETE_REGION}>
        {allBeaches.map((beach) => {
          const series = seriesMap[beach.id]?.series;
          const conditions = series ? pickConditionsForOffset(series, dayOffset) : null;
          const level = conditions ? windLevel(conditions.windSpeedKmh) : null;
          const name = locale === 'el' ? beach.nameEl : beach.nameEn;
          return (
            <Marker
              key={beach.id}
              coordinate={{ latitude: beach.latitude, longitude: beach.longitude }}
              pinColor={level?.color}
            >
              <Callout>
                <View style={styles.callout}>
                  <Text style={styles.calloutTitle}>{name}</Text>
                  <Text style={styles.calloutRegion}>
                    {strings.prefectures[beach.prefecture]}
                    {beach.status === 'pending'
                      ? ` · ${strings.pendingBadge}`
                      : beach.source === 'community'
                        ? ` · ${strings.communityBadge}`
                        : ''}
                  </Text>
                  {conditions && level && (
                    <Text style={[styles.calloutCondition, { color: level.color }]}>
                      {level.dot} {strings.wind[level.key]} · {Math.round(conditions.windSpeedKmh)} km/h{' '}
                      {degreesToCompass(conditions.windDirectionDeg, locale)}
                    </Text>
                  )}
                </View>
              </Callout>
            </Marker>
          );
        })}
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  callout: {
    minWidth: 160,
    padding: 4,
  },
  calloutTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#123',
  },
  calloutRegion: {
    fontSize: 12,
    color: '#678',
    marginBottom: 4,
  },
  calloutCondition: {
    fontSize: 13,
    fontWeight: '600',
  },
});
