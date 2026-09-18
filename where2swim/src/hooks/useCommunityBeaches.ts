import { useCallback, useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';
import { ensureAnonymousUser } from '../lib/auth';
import { Beach, Coast, Prefecture } from '../types/beach';
import { transliterateForDisplay } from '../utils/transliteration';

const HAS_GREEK = /[Ͱ-Ͽἀ-῿]/;

interface CommunityBeachRow {
  id: string;
  name: string;
  prefecture: Prefecture;
  coast: Coast;
  latitude: number;
  longitude: number;
  status: 'pending' | 'approved';
}

function rowToBeach(row: CommunityBeachRow): Beach {
  // Submitters only enter one name; Greek input (the common case, since
  // search/pin results for Crete come back in Greek) gets a Greeklish
  // nameEn generated the same way the seed dataset's does. Latin-only
  // input has no reliable reverse transliteration, so it's kept as-is
  // for both, matching how untranslated seed entries used to render.
  const nameEn = HAS_GREEK.test(row.name) ? transliterateForDisplay(row.name) : row.name;
  return {
    id: `community-${row.id}`,
    nameEl: row.name,
    nameEn,
    prefecture: row.prefecture,
    coast: row.coast,
    latitude: row.latitude,
    longitude: row.longitude,
    source: 'community',
    status: row.status,
  };
}

export function useCommunityBeachesData() {
  const [beaches, setBeaches] = useState<Beach[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    if (!supabase) {
      setLoading(false);
      return;
    }
    setLoading(true);
    // Row-level security only returns approved beaches plus this device's
    // own pending ones — no client-side filtering needed.
    const { data, error } = await supabase
      .from('community_beaches')
      .select('*')
      .order('submitted_at', { ascending: false });

    if (!error && data) {
      setBeaches((data as CommunityBeachRow[]).map(rowToBeach));
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    (async () => {
      await ensureAnonymousUser();
      refresh();
    })();
  }, [refresh]);

  const addBeach = useCallback((beach: Beach) => {
    setBeaches((prev) => [beach, ...prev]);
  }, []);

  return { beaches, loading, refresh, addBeach };
}
