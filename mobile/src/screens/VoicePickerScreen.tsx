import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { getVoiceProfiles } from '../api/profiles';
import { generateStory } from '../api/stories';
import { ChildProfile, Story, VoiceProfile } from '../types';
import StarBackground from '../components/StarBackground';
import curatedStories from '../assets/data/curated_stories.json';

type RootStackParamList = {
  VoicePicker: { profile: ChildProfile; selectedThemes: string[] };
  StoryPlayer: { story: Story };
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
type RoutePropType = RouteProp<RootStackParamList, 'VoicePicker'>;

interface VoiceOption {
  id: string;
  label: string;
  description: string;
  emoji: string;
  voiceId: string;
  isAI: boolean;
}

const DEFAULT_VOICE_OPTIONS: VoiceOption[] = [
  {
    id: 'ai',
    label: 'Story Voice',
    description: 'A warm, magical AI narrator',
    emoji: '✨',
    voiceId: 'elevenlabs_default',
    isAI: true,
  },
];

export default function VoicePickerScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<RoutePropType>();
  const { profile, selectedThemes } = route.params;

  const [voiceOptions, setVoiceOptions] = useState<VoiceOption[]>(DEFAULT_VOICE_OPTIONS);
  const [selectedVoiceId, setSelectedVoiceId] = useState<string>('ai');
  const [isLoadingVoices, setIsLoadingVoices] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    loadVoiceProfiles();
  }, []);

  const loadVoiceProfiles = async () => {
    setIsLoadingVoices(true);
    try {
      const response = await getVoiceProfiles(profile.id);
      const parentVoices: VoiceProfile[] = response.data;
      if (parentVoices && parentVoices.length > 0) {
        const parentOptions: VoiceOption[] = parentVoices.map((v) => ({
          id: v.id,
          label: v.label,
          description: `${v.label}'s recorded voice`,
          emoji: v.label.toLowerCase().includes('mom') ? '👩' : '👨',
          voiceId: v.elevenlabs_voice_id,
          isAI: false,
        }));
        setVoiceOptions([...parentOptions, ...DEFAULT_VOICE_OPTIONS]);
      } else {
        setVoiceOptions(DEFAULT_VOICE_OPTIONS);
      }
    } catch {
      setVoiceOptions(DEFAULT_VOICE_OPTIONS);
    } finally {
      setIsLoadingVoices(false);
    }
  };

  const handleLetsGo = async () => {
    setIsGenerating(true);
    try {
      const response = await generateStory({
        child_name: profile.name,
        themes: selectedThemes,
        child_profile_id: profile.id,
        voice: selectedVoiceId,
      });
      const story: Story = response.data;
      navigation.navigate('StoryPlayer', { story });
    } catch {
      // Fall back to a local curated story that matches themes
      const matching = (curatedStories as any[]).find((s) =>
        s.theme_tags.some((t: string) => selectedThemes.includes(t))
      ) || curatedStories[0];
      navigation.navigate('StoryPlayer', { story: matching as Story });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <LinearGradient
      colors={[COLORS.cream, '#E8F0FF', COLORS.skyBlue]}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0.2, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={8} />

        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
        </View>

        {/* Title */}
        <View style={styles.titleContainer}>
          <Text style={styles.title}>Who should tell</Text>
          <Text style={styles.title}>your story?</Text>
          <Text style={styles.subtitle}>Choose a narrator voice</Text>
        </View>

        {/* Selected themes preview */}
        <View style={styles.themesPreview}>
          <Text style={styles.themesPreviewLabel}>Your story will include: </Text>
          <View style={styles.themesRow}>
            {selectedThemes.map((t) => (
              <View key={t} style={styles.themePill}>
                <Text style={styles.themePillText}>{t}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Voice options */}
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {isLoadingVoices ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color={COLORS.deepIndigo} />
              <Text style={styles.loadingText}>Looking for family voices...</Text>
            </View>
          ) : (
            <>
              {voiceOptions.length === 1 && voiceOptions[0].isAI && (
                <View style={styles.noParentVoicesBanner}>
                  <Text style={styles.noParentVoicesText}>
                    No parent voices recorded yet. Ask a parent to record their voice in Parent Mode!
                  </Text>
                </View>
              )}
              {voiceOptions.map((option) => {
                const isSelected = selectedVoiceId === option.id;
                return (
                  <TouchableOpacity
                    key={option.id}
                    style={[styles.voiceCard, isSelected && styles.voiceCardSelected]}
                    onPress={() => setSelectedVoiceId(option.id)}
                    activeOpacity={0.8}
                  >
                    <View style={[styles.voiceIconContainer, isSelected && styles.voiceIconSelected]}>
                      <Text style={styles.voiceEmoji}>{option.emoji}</Text>
                    </View>
                    <View style={styles.voiceInfo}>
                      <Text style={styles.voiceLabel}>{option.label}</Text>
                      <Text style={styles.voiceDesc}>{option.description}</Text>
                    </View>
                    {isSelected && (
                      <View style={styles.selectedBadge}>
                        <Text style={styles.selectedBadgeText}>✓</Text>
                      </View>
                    )}
                  </TouchableOpacity>
                );
              })}
            </>
          )}
        </ScrollView>

        {/* CTA */}
        <View style={styles.footer}>
          <TouchableOpacity
            style={[styles.goButton, isGenerating && styles.goButtonDisabled]}
            onPress={handleLetsGo}
            activeOpacity={0.8}
            disabled={isGenerating}
          >
            {isGenerating ? (
              <View style={styles.generatingRow}>
                <ActivityIndicator color={COLORS.gold} size="small" />
                <Text style={styles.goButtonText}>  Creating your story...</Text>
              </View>
            ) : (
              <Text style={styles.goButtonText}>Let's Go! 🚀</Text>
            )}
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  safe: {
    flex: 1,
  },
  header: {
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.sm,
  },
  backButton: {
    width: 56,
    height: 56,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.6)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  backButtonText: {
    fontSize: FONTS.sizes.lg,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  titleContainer: {
    paddingHorizontal: SPACING.lg,
    marginTop: SPACING.lg,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    lineHeight: 44,
  },
  subtitle: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
    marginTop: SPACING.xs,
    fontWeight: FONTS.weights.medium as any,
  },
  themesPreview: {
    paddingHorizontal: SPACING.lg,
    marginBottom: SPACING.md,
  },
  themesPreviewLabel: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    marginBottom: SPACING.xs,
  },
  themesRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.xs,
  },
  themePill: {
    backgroundColor: COLORS.lavender,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.md,
    paddingVertical: 4,
  },
  themePillText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
    textTransform: 'capitalize',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.md,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.xxl,
    gap: SPACING.md,
  },
  loadingText: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
    marginTop: SPACING.sm,
  },
  noParentVoicesBanner: {
    backgroundColor: COLORS.peach,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  noParentVoicesText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.darkText,
    lineHeight: 20,
  },
  voiceCard: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.md,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderWidth: 2,
    borderColor: 'transparent',
    minHeight: 80,
  },
  voiceCardSelected: {
    borderColor: COLORS.deepIndigo,
    backgroundColor: '#F0ECFF',
  },
  voiceIconContainer: {
    width: 56,
    height: 56,
    borderRadius: RADIUS.round,
    backgroundColor: COLORS.lavender,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.md,
  },
  voiceIconSelected: {
    backgroundColor: COLORS.deepIndigo,
  },
  voiceEmoji: {
    fontSize: 28,
  },
  voiceInfo: {
    flex: 1,
  },
  voiceLabel: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: 2,
  },
  voiceDesc: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
  },
  selectedBadge: {
    width: 32,
    height: 32,
    borderRadius: RADIUS.round,
    backgroundColor: COLORS.deepIndigo,
    alignItems: 'center',
    justifyContent: 'center',
  },
  selectedBadgeText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.heavy as any,
  },
  footer: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xl,
    paddingTop: SPACING.md,
  },
  goButton: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 64,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 5,
  },
  goButtonDisabled: {
    opacity: 0.7,
  },
  generatingRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  goButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    letterSpacing: 0.5,
  },
});
