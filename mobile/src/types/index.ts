export interface User {
  id: string;
  email: string;
  family_name: string;
  subscription_status: 'trial' | 'active' | 'lapsed';
}

export interface ChildProfile {
  id: string;
  name: string;
  avatar: string; // emoji
  age: number;
  allowed_themes: string[];
  blocked_themes: string[];
  story_intensity: 'calm' | 'moderate' | 'adventurous';
  sleep_timer_default: number;
}

export interface VoiceProfile {
  id: string;
  label: string; // "Mom", "Dad"
  elevenlabs_voice_id: string;
}

export interface StoryPage {
  page_number: number;
  text: string;
  illustration_url: string;
  audio_url?: string;
  emoji?: string;
  bg_color?: string;
}

export interface Story {
  id: string;
  title: string;
  theme_tags: string[];
  pages: StoryPage[];
  duration_seconds: number;
  is_curated: boolean;
  is_ai_generated: boolean;
}

export interface Theme {
  id: string;
  label: string;
  emoji: string;
  color: string;
}
