import React, { useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { ChildProfile } from '../types';
import StarBackground from '../components/StarBackground';
import * as Speech from 'expo-speech';

const { width } = Dimensions.get('window');

type RootStackParamList = {
  StoryModeSelect: { profile: ChildProfile };
  ThemePicker: { profile: ChildProfile };
  StoryLibrary: { profile: ChildProfile };
  ParentPasscode: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
type RoutePropType = RouteProp<RootStackParamList, 'StoryModeSelect'>;

export default function StoryModeSelectScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<RoutePropType>();
  const { profile } = route.params;

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  useEffect(() => {
    const greeting = `${getGreeting()}, ${profile.name}! Ready for a bedtime story?`;
    const timer = setTimeout(() => {
      Speech.speak(greeting, { rate: 0.78, pitch: 1.0 });
    }, 400);
    return () => {
      clearTimeout(timer);
      Speech.stop();
    };
  }, []);

  return (
    <LinearGradient
      colors={[COLORS.cream, '#E8F4FF', COLORS.skyBlue]}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0.2, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={10} />

        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.parentButton}
            onPress={() => navigation.navigate('ParentPasscode')}
            activeOpacity={0.8}
          >
            <Text style={styles.parentButtonText}>🔐</Text>
          </TouchableOpacity>
        </View>

        {/* Greeting */}
        <View style={styles.greetingContainer}>
          <Text style={styles.greetingText}>
            {getGreeting()},{'\n'}
            <Text style={styles.greetingName}>{profile.name}!</Text>
          </Text>
          <Text style={styles.greetingMoon}> 🌙</Text>
        </View>
        <Text style={styles.subheading}>What would you like to do?</Text>

        {/* Mode Cards */}
        <View style={styles.cardsContainer}>
          {/* Pick a Story */}
          <TouchableOpacity
            style={styles.modeCard}
            onPress={() => navigation.navigate('StoryLibrary', { profile })}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={[COLORS.gold, '#FFECA0']}
              style={styles.modeCardGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              <Text style={styles.modeCardEmoji}>📚</Text>
              <Text style={styles.modeCardTitle}>Pick a Story</Text>
              <Text style={styles.modeCardDesc}>
                Choose from our magical library of bedtime tales
              </Text>
              <View style={styles.modeCardArrow}>
                <Text style={styles.modeCardArrowText}>→</Text>
              </View>
            </LinearGradient>
          </TouchableOpacity>

          {/* Make a Story */}
          <TouchableOpacity
            style={styles.modeCard}
            onPress={() => navigation.navigate('ThemePicker', { profile })}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={[COLORS.lavender, '#E4D8FF']}
              style={styles.modeCardGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              <Text style={styles.modeCardEmoji}>✨</Text>
              <Text style={styles.modeCardTitle}>Make a Story</Text>
              <Text style={styles.modeCardDesc}>
                Create your very own magical adventure with AI
              </Text>
              <View style={styles.modeCardArrow}>
                <Text style={styles.modeCardArrowText}>→</Text>
              </View>
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Avatar & name at bottom */}
        <View style={styles.profilePeek}>
          <Text style={styles.profilePeekAvatar}>{profile.avatar}</Text>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.sm,
    paddingBottom: SPACING.sm,
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
  parentButton: {
    width: 56,
    height: 56,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.6)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  parentButtonText: {
    fontSize: 24,
  },
  greetingContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: SPACING.lg,
    marginTop: SPACING.lg,
  },
  greetingText: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    lineHeight: 46,
  },
  greetingName: {
    color: COLORS.deepIndigo,
  },
  greetingMoon: {
    fontSize: FONTS.sizes.xl,
    marginBottom: SPACING.xs,
  },
  subheading: {
    fontSize: FONTS.sizes.md,
    color: COLORS.mutedText,
    paddingHorizontal: SPACING.lg,
    marginTop: SPACING.sm,
    marginBottom: SPACING.xl,
    fontWeight: FONTS.weights.medium as any,
  },
  cardsContainer: {
    paddingHorizontal: SPACING.lg,
    gap: SPACING.md,
    flex: 1,
  },
  modeCard: {
    borderRadius: RADIUS.lg,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.18,
    shadowRadius: 14,
    elevation: 6,
    overflow: 'hidden',
    flex: 1,
  },
  modeCardGradient: {
    flex: 1,
    padding: SPACING.xl,
    justifyContent: 'center',
  },
  modeCardEmoji: {
    fontSize: 56,
    marginBottom: SPACING.md,
  },
  modeCardTitle: {
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.sm,
  },
  modeCardDesc: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
    lineHeight: 24,
    fontWeight: FONTS.weights.medium as any,
    maxWidth: '80%',
  },
  modeCardArrow: {
    position: 'absolute',
    right: SPACING.xl,
    bottom: SPACING.xl,
    width: 44,
    height: 44,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.7)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  modeCardArrowText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  profilePeek: {
    alignItems: 'center',
    paddingBottom: SPACING.xl,
    paddingTop: SPACING.md,
  },
  profilePeekAvatar: {
    fontSize: 48,
    opacity: 0.5,
  },
});
