import { createContext, ReactNode, useContext } from 'react';
import { useFavoritesData } from '../hooks/useFavorites';

interface FavoritesContextValue {
  favorites: Set<string>;
  loaded: boolean;
  toggleFavorite: (id: string) => void;
}

const FavoritesContext = createContext<FavoritesContextValue | null>(null);

export function FavoritesProvider({ children }: { children: ReactNode }) {
  const value = useFavoritesData();
  return <FavoritesContext.Provider value={value}>{children}</FavoritesContext.Provider>;
}

export function useFavorites() {
  const ctx = useContext(FavoritesContext);
  if (!ctx) throw new Error('useFavorites must be used within FavoritesProvider');
  return ctx;
}
