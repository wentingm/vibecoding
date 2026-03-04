import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { User } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  loadStoredToken: () => Promise<boolean>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  setAuth: async (user, token) => {
    await SecureStore.setItemAsync('auth_token', token);
    set({ user, token });
  },
  logout: async () => {
    await SecureStore.deleteItemAsync('auth_token');
    set({ user: null, token: null });
  },
  loadStoredToken: async () => {
    const token = await SecureStore.getItemAsync('auth_token');
    if (token) {
      set({ token });
      return true;
    }
    return false;
  },
}));
