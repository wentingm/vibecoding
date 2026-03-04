import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { createProfile } from '../api/profiles';
import { useProfileStore } from '../store/profileStore';

type RootStackParamList = {
  ProfileSelect: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

const AVATAR_OPTIONS = ['🦁', '🐬', '🦊', '🐼', '🦋', '🐸', '🦄', '🐧', '🐻', '🦸', '🧸', '🐯'];
const TIMER_OPTIONS = [5, 10, 15, 30];
const MIN_AGE = 2;
const MAX_AGE = 12;

export default function AddProfileScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { profiles, setProfiles } = useProfileStore();

  const [selectedAvatar, setSelectedAvatar] = useState(AVATAR_OPTIONS[0]);
  const [name, setName] = useState('');
  const [age, setAge] = useState(4);
  const [sleepTimer, setSleepTimer] = useState(15);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const incrementAge = async () => {
    if (age < MAX_AGE) {
      if (Platform.OS !== 'web') await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      setAge((prev) => prev + 1);
    }
  };

  const decrementAge = async () => {
    if (age > MIN_AGE) {
      if (Platform.OS !== 'web') await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      setAge((prev) => prev - 1);
    }
  };

  const handleSave = async () => {
    if (!name.trim()) {
      setError("Please enter your little dreamer's name!");
      return;
    }
    setIsLoading(true);
    setError('');

    const profileData = {
      name: name.trim(),
      avatar: selectedAvatar,
      age,
      sleep_timer_default: sleepTimer,
      story_intensity: 'calm' as const,
      allowed_themes: [],
      blocked_themes: [],
    };

    try {
      const response = await createProfile(profileData);
      const newProfile = response.data;
      setProfiles([...profiles, newProfile]);
      navigation.navigate('ProfileSelect');
    } catch {
      // Add locally as fallback
      const localProfile = {
        ...profileData,
        id: `local_${Date.now()}`,
      };
      setProfiles([...profiles, localProfile]);
      navigation.navigate('ProfileSelect');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={[COLORS.cream, '#FFF0E8', COLORS.peach]}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.safe}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Add a Little Dreamer</Text>
          <View style={styles.headerRight} />
        </View>

        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {/* Avatar picker */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Choose an avatar</Text>
            <View style={styles.selectedAvatarContainer}>
              <Text style={styles.selectedAvatarEmoji}>{selectedAvatar}</Text>
            </View>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.avatarRow}
            >
              {AVATAR_OPTIONS.map((emoji) => (
                <TouchableOpacity
                  key={emoji}
                  style={[
                    styles.avatarOption,
                    selectedAvatar === emoji && styles.avatarOptionSelected,
                  ]}
                  onPress={() => setSelectedAvatar(emoji)}
                  activeOpacity={0.8}
                >
                  <Text style={styles.avatarOptionEmoji}>{emoji}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>

          {/* Name input */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Name</Text>
            <TextInput
              style={styles.nameInput}
              placeholder="e.g. Lucas or Olivia"
              placeholderTextColor={COLORS.mutedText}
              value={name}
              onChangeText={setName}
              autoCapitalize="words"
              returnKeyType="done"
              maxLength={20}
            />
          </View>

          {/* Age picker */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Age</Text>
            <View style={styles.agePicker}>
              <TouchableOpacity
                style={[styles.ageButton, age <= MIN_AGE && styles.ageButtonDisabled]}
                onPress={decrementAge}
                activeOpacity={0.8}
                disabled={age <= MIN_AGE}
              >
                <Text style={styles.ageButtonText}>−</Text>
              </TouchableOpacity>
              <View style={styles.ageDisplay}>
                <Text style={styles.ageValue}>{age}</Text>
                <Text style={styles.ageUnit}>years old</Text>
              </View>
              <TouchableOpacity
                style={[styles.ageButton, age >= MAX_AGE && styles.ageButtonDisabled]}
                onPress={incrementAge}
                activeOpacity={0.8}
                disabled={age >= MAX_AGE}
              >
                <Text style={styles.ageButtonText}>+</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Sleep timer */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Default sleep timer</Text>
            <View style={styles.timerOptions}>
              {TIMER_OPTIONS.map((mins) => (
                <TouchableOpacity
                  key={mins}
                  style={[
                    styles.timerOption,
                    sleepTimer === mins && styles.timerOptionSelected,
                  ]}
                  onPress={() => setSleepTimer(mins)}
                  activeOpacity={0.8}
                >
                  <Text
                    style={[
                      styles.timerOptionText,
                      sleepTimer === mins && styles.timerOptionTextSelected,
                    ]}
                  >
                    {mins} min
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Error */}
          {error ? (
            <View style={styles.errorBanner}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          {/* Save button */}
          <TouchableOpacity
            style={[styles.saveButton, isLoading && styles.saveButtonDisabled]}
            onPress={handleSave}
            activeOpacity={0.8}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color={COLORS.gold} />
            ) : (
              <Text style={styles.saveButtonText}>Save Profile ✨</Text>
            )}
          </TouchableOpacity>

          <View style={styles.bottomSpacing} />
        </ScrollView>
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
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.sm,
    paddingBottom: SPACING.md,
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
  headerTitle: {
    flex: 1,
    textAlign: 'center',
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  headerRight: {
    width: 56,
  },
  scrollContent: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xl,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionLabel: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.md,
  },
  selectedAvatarContainer: {
    width: 100,
    height: 100,
    borderRadius: RADIUS.xl,
    backgroundColor: COLORS.white,
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
    marginBottom: SPACING.md,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 4,
  },
  selectedAvatarEmoji: {
    fontSize: 64,
  },
  avatarRow: {
    paddingRight: SPACING.lg,
    gap: SPACING.sm,
  },
  avatarOption: {
    width: 64,
    height: 64,
    borderRadius: RADIUS.md,
    backgroundColor: COLORS.white,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 2,
  },
  avatarOptionSelected: {
    borderColor: COLORS.deepIndigo,
    backgroundColor: COLORS.lavender,
  },
  avatarOptionEmoji: {
    fontSize: 36,
  },
  nameInput: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.md,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    fontSize: FONTS.sizes.md,
    color: COLORS.darkText,
    borderWidth: 2,
    borderColor: COLORS.lavender,
    minHeight: 60,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 6,
    elevation: 2,
  },
  agePicker: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: SPACING.xl,
  },
  ageButton: {
    width: 72,
    height: 72,
    borderRadius: RADIUS.round,
    backgroundColor: COLORS.deepIndigo,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 4,
  },
  ageButtonDisabled: {
    opacity: 0.3,
  },
  ageButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    lineHeight: FONTS.sizes.xl + 4,
  },
  ageDisplay: {
    alignItems: 'center',
    minWidth: 80,
  },
  ageValue: {
    fontSize: FONTS.sizes.xxl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    lineHeight: FONTS.sizes.xxl + 4,
  },
  ageUnit: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
    marginTop: 2,
  },
  timerOptions: {
    flexDirection: 'row',
    gap: SPACING.sm,
    flexWrap: 'wrap',
  },
  timerOption: {
    flex: 1,
    minWidth: 70,
    paddingVertical: SPACING.md,
    borderRadius: RADIUS.md,
    backgroundColor: COLORS.white,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.lavender,
    minHeight: 52,
    justifyContent: 'center',
  },
  timerOptionSelected: {
    backgroundColor: COLORS.deepIndigo,
    borderColor: COLORS.deepIndigo,
  },
  timerOptionText: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
  },
  timerOptionTextSelected: {
    color: COLORS.gold,
  },
  errorBanner: {
    backgroundColor: '#FFEBEE',
    borderRadius: RADIUS.sm,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
  },
  errorText: {
    color: '#C62828',
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.medium as any,
  },
  saveButton: {
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
  saveButtonDisabled: {
    opacity: 0.7,
  },
  saveButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    letterSpacing: 0.5,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});
