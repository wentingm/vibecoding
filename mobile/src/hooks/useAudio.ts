// Safe audio hook — no-ops gracefully when expo-av isn't available (Expo Go)
let Audio: any = null;
try {
  Audio = require('expo-av').Audio;
  console.log('[useAudio] expo-av loaded successfully, Audio:', !!Audio);
} catch (e) {
  console.log('[useAudio] expo-av failed to load:', e);
}

export { Audio };

export const isAudioAvailable = !!Audio;
