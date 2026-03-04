import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  FlatList,
  ActivityIndicator,
  Dimensions,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { getProfiles } from '../api/profiles';
import { useProfileStore } from '../store/profileStore';
import { ChildProfile } from '../types';
import StarBackground from '../components/StarBackground';

const { width } = Dimensions.get('window');
const TILE_SIZE = (width - SPACING.lg * 2 - SPACING.md) / 2;

const MOCK_PROFILES: ChildProfile[] = [
  {
    id: 'mock_1',
    name: 'Lucas',
    avatar: '🦁',
    age: 5,
    allowed_themes: ['dragon', 'space', 'animals'],
    blocked_themes: [],
    story_intensity: 'moderate',
    sleep_timer_default: 15,
  },
  {
    id: 'mock_2',
    name: 'Olivia',
    avatar: '🦄',
    age: 4,
    allowed_themes: ['fairy', 'magic', 'unicorn'],
    blocked_themes: [],
    story_intensity: 'calm',
    sleep_timer_default: 10,
  },
];

const TILE_COLORS = [
  COLORS.lavender, COLORS.gold, COLORS.skyBlue,
  COLORS.rose, COLORS.mint, COLORS.peach,
];

type RootStackParamList = {
  StoryModeSelect: { profile: ChildProfile };
  ParentPasscode: undefined;
  AddProfile: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function ProfileSelectScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { profiles, setProfiles, setActiveProfile } = useProfileStore();
  const [isLoading, setIsLoading] = useState(true);

  const loadProfiles = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await getProfiles();
      const fetchedProfiles: ChildProfile[] = response.data;
      if (fetchedProfiles.length > 0) {
        setProfiles(fetchedProfiles);
      } else {
        setProfiles(MOCK_PROFILES);
      }
    } catch {
      setProfiles(MOCK_PROFILES);
    } finally {
      setIsLoading(false);
    }
  }, [setProfiles]);

  useEffect(() => {
    loadProfiles();
  }, [loadProfiles]);

  const handleProfileSelect = async (profile: ChildProfile) => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
    setActiveProfile(profile);
    navigation.navigate('StoryModeSelect', { profile });
  };

  const renderProfileTile = ({ item, index }: { item: ChildProfile | 'add'; index: number }) => {
    if (item === 'add') {
      return (
        <TouchableOpacity
          style={[styles.tile, styles.addTile]}
          onPress={() => navigation.navigate('AddProfile')}
          activeOpacity={0.8}
        >
          <Text style={styles.addTileIcon}>+</Text>
          <Text style={styles.addTileLabel}>Add Child</Text>
        </TouchableOpacity>
      );
    }

    const profile = item as ChildProfile;
    const bgColor = TILE_COLORS[index % TILE_COLORS.length];

    return (
      <TouchableOpacity
        style={[styles.tile, { backgroundColor: bgColor }]}
        onPress={() => handleProfileSelect(profile)}
        activeOpacity={0.8}
      >
        <Text style={styles.profileAvatar}>{profile.avatar}</Text>
        <Text style={styles.profileName}>{profile.name}</Text>
        <Text style={styles.profileAge}>Age {profile.age}</Text>
      </TouchableOpacity>
    );
  };

  const listData: (ChildProfile | 'add')[] = [...profiles, 'add'];

  return (
    <LinearGradient
      colors={[COLORS.cream, '#EEE4FF', COLORS.lavender]}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0.3, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={12} />

        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerLeft} />
          <View style={styles.headerCenter}>
            <Text style={styles.headerEmoji}>🌙</Text>
          </View>
          <TouchableOpacity
            style={styles.parentButton}
            onPress={() => navigation.navigate('ParentPasscode')}
            activeOpacity={0.8}
          >
            <Text style={styles.parentButtonText}>🔐</Text>
          </TouchableOpacity>
        </View>

        {/* Title */}
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>Who's ready</Text>
          <Text style={styles.titleText}>for a story? 📖</Text>
        </View>

        {/* Profiles grid */}
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={COLORS.deepIndigo} />
            <Text style={styles.loadingText}>Waking up the dreamers...</Text>
          </View>
        ) : (
          <FlatList
            data={listData}
            renderItem={renderProfileTile}
            keyExtractor={(item, index) =>
              item === 'add' ? 'add' : (item as ChildProfile).id
            }
            numColumns={2}
            contentContainerStyle={styles.grid}
            columnWrapperStyle={styles.row}
            showsVerticalScrollIndicator={false}
          />
        )}
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
  headerLeft: {
    width: 56,
  },
  headerCenter: {
    alignItems: 'center',
  },
  headerEmoji: {
    fontSize: 32,
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
  titleContainer: {
    paddingHorizontal: SPACING.lg,
    marginBottom: SPACING.xl,
    marginTop: SPACING.sm,
  },
  titleText: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    lineHeight: 46,
  },
  grid: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  row: {
    justifyContent: 'space-between',
    marginBottom: SPACING.md,
  },
  tile: {
    width: TILE_SIZE,
    height: TILE_SIZE,
    borderRadius: RADIUS.lg,
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.md,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 5,
  },
  addTile: {
    backgroundColor: 'rgba(255,255,255,0.7)',
    borderWidth: 3,
    borderColor: COLORS.lavender,
    borderStyle: 'dashed',
  },
  addTileIcon: {
    fontSize: 40,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.bold as any,
    lineHeight: 48,
  },
  addTileLabel: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
    marginTop: SPACING.xs,
  },
  profileAvatar: {
    fontSize: 60,
    marginBottom: SPACING.sm,
  },
  profileName: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  profileAge: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
    marginTop: 2,
  },
  loadingContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: SPACING.md,
  },
  loadingText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
    marginTop: SPACING.sm,
  },
});
