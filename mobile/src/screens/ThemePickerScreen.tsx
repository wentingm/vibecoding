import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  FlatList,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { STORY_THEMES } from '../constants/themes';
import { ChildProfile } from '../types';
import StarBackground from '../components/StarBackground';

type RootStackParamList = {
  ThemePicker: { profile: ChildProfile };
  VoicePicker: { profile: ChildProfile; selectedThemes: string[] };
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
type RoutePropType = RouteProp<RootStackParamList, 'ThemePicker'>;

const MAX_THEMES = 3;

export default function ThemePickerScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<RoutePropType>();
  const { profile } = route.params;
  const [selectedThemes, setSelectedThemes] = useState<string[]>([]);

  const toggleTheme = async (themeId: string) => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    setSelectedThemes((prev) => {
      if (prev.includes(themeId)) {
        return prev.filter((id) => id !== themeId);
      }
      if (prev.length >= MAX_THEMES) return prev;
      return [...prev, themeId];
    });
  };

  const handleCreate = () => {
    if (selectedThemes.length === 0) return;
    navigation.navigate('VoicePicker', { profile, selectedThemes });
  };

  const renderThemeTile = ({ item }: { item: typeof STORY_THEMES[0] }) => {
    const isSelected = selectedThemes.includes(item.id);
    const isDisabled = !isSelected && selectedThemes.length >= MAX_THEMES;

    return (
      <TouchableOpacity
        style={[
          styles.themeTile,
          { backgroundColor: item.color },
          isSelected && styles.themeTileSelected,
          isDisabled && styles.themeTileDisabled,
        ]}
        onPress={() => toggleTheme(item.id)}
        activeOpacity={0.8}
      >
        {isSelected && (
          <View style={styles.checkOverlay}>
            <Text style={styles.checkMark}>✓</Text>
          </View>
        )}
        <Text style={styles.themeEmoji}>{item.emoji}</Text>
        <Text style={styles.themeLabel}>{item.label}</Text>
      </TouchableOpacity>
    );
  };

  return (
    <LinearGradient
      colors={[COLORS.cream, '#FFF0E8', COLORS.peach]}
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
          <Text style={styles.title}>What's your</Text>
          <Text style={styles.title}>story about?</Text>
          <Text style={styles.subtitle}>Pick up to 3 things you love!</Text>
        </View>

        {/* Selection counter */}
        <View style={styles.counterRow}>
          <View style={styles.counterBadge}>
            <Text style={styles.counterText}>
              {selectedThemes.length} of {MAX_THEMES} chosen
            </Text>
          </View>
          {[0, 1, 2].map((i) => (
            <View
              key={i}
              style={[
                styles.counterDot,
                selectedThemes.length > i && styles.counterDotFilled,
              ]}
            />
          ))}
        </View>

        {/* Theme grid */}
        <FlatList
          data={STORY_THEMES}
          renderItem={renderThemeTile}
          keyExtractor={(item) => item.id}
          numColumns={3}
          contentContainerStyle={styles.grid}
          columnWrapperStyle={styles.row}
          showsVerticalScrollIndicator={false}
        />

        {/* CTA Button */}
        <View style={styles.footer}>
          <TouchableOpacity
            style={[
              styles.createButton,
              selectedThemes.length === 0 && styles.createButtonDisabled,
            ]}
            onPress={handleCreate}
            activeOpacity={0.8}
            disabled={selectedThemes.length === 0}
          >
            <Text style={styles.createButtonText}>Create My Story! ✨</Text>
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
  counterRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    marginBottom: SPACING.md,
    gap: SPACING.xs,
  },
  counterBadge: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    marginRight: SPACING.sm,
  },
  counterText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.bold as any,
  },
  counterDot: {
    width: 10,
    height: 10,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(45,27,105,0.2)',
  },
  counterDotFilled: {
    backgroundColor: COLORS.deepIndigo,
  },
  grid: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.md,
  },
  row: {
    justifyContent: 'space-between',
    marginBottom: SPACING.sm,
  },
  themeTile: {
    width: '31%',
    aspectRatio: 1,
    borderRadius: RADIUS.md,
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.sm,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 3,
    overflow: 'hidden',
  },
  themeTileSelected: {
    borderWidth: 3,
    borderColor: COLORS.gold,
  },
  themeTileDisabled: {
    opacity: 0.4,
  },
  checkOverlay: {
    position: 'absolute',
    top: 6,
    right: 6,
    width: 22,
    height: 22,
    borderRadius: RADIUS.round,
    backgroundColor: COLORS.gold,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkMark: {
    fontSize: 12,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.heavy as any,
  },
  themeEmoji: {
    fontSize: 36,
    marginBottom: SPACING.xs,
  },
  themeLabel: {
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
    textAlign: 'center',
  },
  footer: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xl,
    paddingTop: SPACING.md,
  },
  createButton: {
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
  createButtonDisabled: {
    opacity: 0.4,
  },
  createButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    letterSpacing: 0.5,
  },
});
