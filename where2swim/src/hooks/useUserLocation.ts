import { useCallback, useState } from 'react';
import * as Location from 'expo-location';

export type LocationStatus = 'idle' | 'requesting' | 'granted' | 'denied';

export interface UserCoords {
  latitude: number;
  longitude: number;
}

export function useUserLocation() {
  const [status, setStatus] = useState<LocationStatus>('idle');
  const [coords, setCoords] = useState<UserCoords | null>(null);

  const requestLocation = useCallback(async () => {
    setStatus('requesting');
    try {
      const { status: permission } = await Location.requestForegroundPermissionsAsync();
      if (permission !== 'granted') {
        setStatus('denied');
        return;
      }
      const position = await Location.getCurrentPositionAsync({});
      setCoords({ latitude: position.coords.latitude, longitude: position.coords.longitude });
      setStatus('granted');
    } catch {
      setStatus('denied');
    }
  }, []);

  return { status, coords, requestLocation };
}
