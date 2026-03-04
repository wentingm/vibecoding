import { create } from 'zustand';
import { ChildProfile } from '../types';

interface ProfileState {
  profiles: ChildProfile[];
  activeProfile: ChildProfile | null;
  setProfiles: (profiles: ChildProfile[]) => void;
  setActiveProfile: (profile: ChildProfile) => void;
}

export const useProfileStore = create<ProfileState>((set) => ({
  profiles: [],
  activeProfile: null,
  setProfiles: (profiles) => set({ profiles }),
  setActiveProfile: (profile) => set({ activeProfile: profile }),
}));
