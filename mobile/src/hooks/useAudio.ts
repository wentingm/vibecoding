// Safe audio hook — no-ops gracefully when expo-av isn't available (Expo Go)
let Audio: any = null;
try {
  Audio = require('expo-av').Audio;
} catch {}

export { Audio };

export const isAudioAvailable = !!Audio;
