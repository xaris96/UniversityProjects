import { createContext, ReactNode, useContext } from 'react';
import { useCommunityBeachesData } from '../hooks/useCommunityBeaches';
import { Beach } from '../types/beach';

interface CommunityBeachesContextValue {
  beaches: Beach[];
  loading: boolean;
  refresh: () => Promise<void>;
  addBeach: (beach: Beach) => void;
}

const CommunityBeachesContext = createContext<CommunityBeachesContextValue | null>(null);

export function CommunityBeachesProvider({ children }: { children: ReactNode }) {
  const value = useCommunityBeachesData();
  return <CommunityBeachesContext.Provider value={value}>{children}</CommunityBeachesContext.Provider>;
}

export function useCommunityBeaches() {
  const ctx = useContext(CommunityBeachesContext);
  if (!ctx) throw new Error('useCommunityBeaches must be used within CommunityBeachesProvider');
  return ctx;
}
