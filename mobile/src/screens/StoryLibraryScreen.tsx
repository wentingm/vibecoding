import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  FlatList,
  ScrollView,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { STORY_THEMES } from '../constants/themes';
import { getCuratedStories } from '../api/stories';
import { Story, ChildProfile } from '../types';
import curatedStoriesData from '../assets/data/curated_stories.json';
import StarBackground from '../components/StarBackground';

const { width } = Dimensions.get('window');

type RootStackParamList = {
  StoryLibrary: { profile: ChildProfile };
  StoryPlayer: { story: Story };
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
type RoutePropType = RouteProp<RootStackParamList, 'StoryLibrary'>;

const CARD_COLORS = [
  [COLORS.lavender, '#E8DEFF'],
  [COLORS.gold, '#FFECA0'],
  [COLORS.skyBlue, '#D4EFFF'],
  [COLORS.rose, '#FFD4E2'],
  [COLORS.mint, '#D4FFE8'],
  [COLORS.peach, '#FFE4D0'],
];

export default function StoryLibraryScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<RoutePropType>();
  const { profile } = route.params;

  const [stories, setStories] = useState<Story[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedThemeFilter, setSelectedThemeFilter] = useState<string | null>(null);
  const [hasError, setHasError] = useState(false);

  const loadStories = useCallback(async (themeFilter?: string | null) => {
    setIsLoading(true);
    setHasError(false);
    try {
      const themes = themeFilter ? [themeFilter] : undefined;
      const response = await getCuratedStories(themes);
      const fetchedStories: Story[] = response.data;
      if (fetchedStories.length > 0) {
        setStories(fetchedStories);
      } else {
        setStories(curatedStoriesData as Story[]);
      }
    } catch {
      // Use local fallback
      const local = curatedStoriesData as Story[];
      if (themeFilter) {
        const filtered = local.filter((s) => s.theme_tags.includes(themeFilter));
        setStories(filtered.length > 0 ? filtered : local);
      } else {
        setStories(local);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadStories(selectedThemeFilter);
  }, [selectedThemeFilter, loadStories]);

  const formatDuration = (seconds: number) => {
    const mins = Math.ceil(seconds / 60);
    return `${mins} min`;
  };

  const renderStoryCard = ({ item, index }: { item: Story; index: number }) => {
    const colors = CARD_COLORS[index % CARD_COLORS.length];
    const firstPage = item.pages?.[0];
    const emoji = (firstPage as any)?.emoji || '📖';

    return (
      <TouchableOpacity
        style={styles.storyCard}
        onPress={() => navigation.navigate('StoryPlayer', { story: item })}
        activeOpacity={0.8}
      >
        {/* Illustration area */}
        <LinearGradient
          colors={[colors[0], colors[1]]}
          style={styles.storyIllustration}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Text style={styles.storyEmoji}>{emoji}</Text>
        </LinearGradient>

        {/* Story info */}
        <View style={styles.storyInfo}>
          <Text style={styles.storyTitle} numberOfLines={2}>
            {item.title}
          </Text>

          <View style={styles.storyMeta}>
            <View style={styles.durationBadge}>
              <Text style={styles.durationText}>🕐 {formatDuration(item.duration_seconds)}</Text>
            </View>
            {item.is_curated && (
              <View style={styles.curatedBadge}>
                <Text style={styles.curatedText}>✨ Staff Pick</Text>
              </View>
            )}
          </View>

          <View style={styles.themeTags}>
            {item.theme_tags.slice(0, 3).map((tag) => (
              <View key={tag} style={styles.themeTag}>
                <Text style={styles.themeTagText}>{tag}</Text>
              </View>
            ))}
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  const allThemes = [{ id: 'all', label: 'All', emoji: '📚', color: COLORS.lavender }, ...STORY_THEMES];

  return (
    <LinearGradient
      colors={[COLORS.cream, '#FFF0E8']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={6} />

        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Story Library 📚</Text>
          <View style={styles.headerRight} />
        </View>

        {/* Theme filter chips */}
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.filterChips}
          style={styles.filterRow}
        >
          {allThemes.map((theme) => {
            const isActive =
              theme.id === 'all'
                ? selectedThemeFilter === null
                : selectedThemeFilter === theme.id;
            return (
              <TouchableOpacity
                key={theme.id}
                style={[styles.filterChip, isActive && styles.filterChipActive]}
                onPress={() =>
                  setSelectedThemeFilter(theme.id === 'all' ? null : theme.id)
                }
                activeOpacity={0.8}
              >
                <Text style={styles.filterChipEmoji}>{theme.emoji}</Text>
                <Text style={[styles.filterChipText, isActive && styles.filterChipTextActive]}>
                  {theme.label}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>

        {/* Stories list */}
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={COLORS.deepIndigo} />
            <Text style={styles.loadingText}>Finding your stories...</Text>
          </View>
        ) : stories.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyEmoji}>🔍</Text>
            <Text style={styles.emptyText}>No stories found for that theme!</Text>
            <TouchableOpacity
              onPress={() => setSelectedThemeFilter(null)}
              activeOpacity={0.8}
            >
              <Text style={styles.emptyLink}>Show all stories</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <FlatList
            data={stories}
            renderItem={renderStoryCard}
            keyExtractor={(item) => item.id}
            contentContainerStyle={styles.storiesList}
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
  headerTitle: {
    flex: 1,
    textAlign: 'center',
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  headerRight: {
    width: 56,
  },
  filterRow: {
    maxHeight: 60,
    marginBottom: SPACING.sm,
  },
  filterChips: {
    paddingHorizontal: SPACING.lg,
    gap: SPACING.xs,
    paddingRight: SPACING.xl,
  },
  filterChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.7)',
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderWidth: 2,
    borderColor: 'transparent',
    gap: 4,
    height: 44,
  },
  filterChipActive: {
    backgroundColor: COLORS.deepIndigo,
    borderColor: COLORS.deepIndigo,
  },
  filterChipEmoji: {
    fontSize: 16,
  },
  filterChipText: {
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
  },
  filterChipTextActive: {
    color: COLORS.gold,
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
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: SPACING.md,
  },
  emptyEmoji: {
    fontSize: 48,
  },
  emptyText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
  },
  emptyLink: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
    textDecorationLine: 'underline',
  },
  storiesList: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  storyCard: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.lg,
    marginBottom: SPACING.md,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    elevation: 4,
    overflow: 'hidden',
    flexDirection: 'row',
  },
  storyIllustration: {
    width: 110,
    minHeight: 110,
    alignItems: 'center',
    justifyContent: 'center',
  },
  storyEmoji: {
    fontSize: 52,
  },
  storyInfo: {
    flex: 1,
    padding: SPACING.md,
    justifyContent: 'center',
  },
  storyTitle: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.xs,
    lineHeight: 28,
  },
  storyMeta: {
    flexDirection: 'row',
    gap: SPACING.xs,
    marginBottom: SPACING.xs,
    flexWrap: 'wrap',
  },
  durationBadge: {
    backgroundColor: COLORS.cream,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 3,
  },
  durationText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    fontWeight: FONTS.weights.medium as any,
  },
  curatedBadge: {
    backgroundColor: COLORS.gold,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 3,
  },
  curatedText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  themeTags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 4,
  },
  themeTag: {
    backgroundColor: COLORS.lavender,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
  },
  themeTagText: {
    fontSize: 11,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.medium as any,
    textTransform: 'capitalize',
  },
});
