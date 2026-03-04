import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Switch,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { useAuthStore } from '../store/authStore';
import { useProfileStore } from '../store/profileStore';
import { getProfiles } from '../api/profiles';
import { ChildProfile } from '../types';
import curatedStoriesData from '../assets/data/curated_stories.json';

type RootStackParamList = {
  ProfileSelect: undefined;
  AddProfile: undefined;
  Login: undefined;
  VoiceUpload: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

interface ChildStats {
  profile: ChildProfile;
  storiesThisWeek: number;
  totalMinutes: number;
  lastActive: string;
}

const MOCK_STATS = (profile: ChildProfile): ChildStats => ({
  profile,
  storiesThisWeek: Math.floor(Math.random() * 5) + 1,
  totalMinutes: Math.floor(Math.random() * 60) + 10,
  lastActive: 'Tonight',
});

export default function ParentDashboardScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { user, logout } = useAuthStore();
  const { profiles, setProfiles } = useProfileStore();
  const [childStats, setChildStats] = useState<ChildStats[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [contentGuardrails, setContentGuardrails] = useState(true);
  const [nightModeAuto, setNightModeAuto] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const response = await getProfiles();
      const fetchedProfiles: ChildProfile[] = response.data;
      if (fetchedProfiles.length > 0) {
        setProfiles(fetchedProfiles);
        setChildStats(fetchedProfiles.map(MOCK_STATS));
      } else if (profiles.length > 0) {
        setChildStats(profiles.map(MOCK_STATS));
      } else {
        // Use some default mock stats
        const mockProfiles: ChildProfile[] = [
          {
            id: 'mock_1',
            name: 'Lucas',
            avatar: '🦁',
            age: 5,
            allowed_themes: [],
            blocked_themes: [],
            story_intensity: 'moderate',
            sleep_timer_default: 15,
          },
        ];
        setChildStats(mockProfiles.map(MOCK_STATS));
      }
    } catch {
      if (profiles.length > 0) {
        setChildStats(profiles.map(MOCK_STATS));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignOut = async () => {
    await logout();
    navigation.navigate('Login');
  };

  const subscriptionLabel = () => {
    switch (user?.subscription_status) {
      case 'active': return { text: 'Active', color: '#4CAF50' };
      case 'trial': return { text: 'Free Trial', color: COLORS.gold };
      case 'lapsed': return { text: 'Expired', color: '#F44336' };
      default: return { text: 'Free Trial', color: COLORS.gold };
    }
  };

  const subStatus = subscriptionLabel();

  return (
    <LinearGradient
      colors={[COLORS.cream, '#EEF2FF']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.safe}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.navigate('ProfileSelect')}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Family Dashboard</Text>
          <Text style={styles.headerEmoji}>👨‍👩‍👧‍👦</Text>
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* Family name */}
          <View style={styles.familyBanner}>
            <View>
              <Text style={styles.familyLabel}>Welcome back,</Text>
              <Text style={styles.familyName}>
                The {user?.family_name || 'Family'}
              </Text>
            </View>
            <View style={[styles.subBadge, { backgroundColor: subStatus.color + '20' }]}>
              <Text style={[styles.subBadgeText, { color: subStatus.color }]}>
                {subStatus.text}
              </Text>
            </View>
          </View>

          {/* Section: Children */}
          <Text style={styles.sectionTitle}>Your Dreamers</Text>

          {isLoading ? (
            <ActivityIndicator color={COLORS.deepIndigo} size="large" style={styles.loader} />
          ) : (
            childStats.map((stat) => (
              <View key={stat.profile.id} style={styles.childCard}>
                <View style={styles.childCardHeader}>
                  <Text style={styles.childAvatar}>{stat.profile.avatar}</Text>
                  <View style={styles.childInfo}>
                    <Text style={styles.childName}>{stat.profile.name}</Text>
                    <Text style={styles.childAge}>Age {stat.profile.age}</Text>
                  </View>
                  <View style={[styles.lastActiveBadge]}>
                    <Text style={styles.lastActiveText}>{stat.lastActive}</Text>
                  </View>
                </View>

                <View style={styles.statsRow}>
                  <View style={styles.statItem}>
                    <Text style={styles.statValue}>{stat.storiesThisWeek}</Text>
                    <Text style={styles.statLabel}>Stories{'\n'}this week</Text>
                  </View>
                  <View style={styles.statDivider} />
                  <View style={styles.statItem}>
                    <Text style={styles.statValue}>{stat.totalMinutes}</Text>
                    <Text style={styles.statLabel}>Minutes{'\n'}total</Text>
                  </View>
                  <View style={styles.statDivider} />
                  <View style={styles.statItem}>
                    <Text style={styles.statValue}>{stat.profile.sleep_timer_default}</Text>
                    <Text style={styles.statLabel}>Timer{'\n'}(min)</Text>
                  </View>
                </View>

                <TouchableOpacity
                  style={styles.manageVoiceButton}
                  activeOpacity={0.8}
                  onPress={() => navigation.navigate('VoiceUpload')}
                >
                  <Text style={styles.manageVoiceText}>🎙 Manage Voices</Text>
                </TouchableOpacity>
              </View>
            ))
          )}

          {/* Add profile button */}
          <TouchableOpacity
            style={styles.addProfileButton}
            onPress={() => navigation.navigate('AddProfile')}
            activeOpacity={0.8}
          >
            <Text style={styles.addProfileButtonText}>+ Add a Child Profile</Text>
          </TouchableOpacity>

          {/* Section: Settings */}
          <Text style={styles.sectionTitle}>Settings</Text>
          <View style={styles.settingsCard}>
            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Content Guardrails</Text>
                <Text style={styles.settingDesc}>Filter out scary content</Text>
              </View>
              <Switch
                value={contentGuardrails}
                onValueChange={setContentGuardrails}
                trackColor={{ false: '#DDD', true: COLORS.lavender }}
                thumbColor={contentGuardrails ? COLORS.deepIndigo : '#FFF'}
              />
            </View>

            <View style={styles.settingDivider} />

            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Auto Night Mode</Text>
                <Text style={styles.settingDesc}>Dim screen after stories</Text>
              </View>
              <Switch
                value={nightModeAuto}
                onValueChange={setNightModeAuto}
                trackColor={{ false: '#DDD', true: COLORS.lavender }}
                thumbColor={nightModeAuto ? COLORS.deepIndigo : '#FFF'}
              />
            </View>

            <View style={styles.settingDivider} />

            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Subscription</Text>
                <Text style={[styles.settingDesc, { color: subStatus.color }]}>
                  {subStatus.text}
                </Text>
              </View>
              <TouchableOpacity
                style={styles.manageSubButton}
                activeOpacity={0.8}
              >
                <Text style={styles.manageSubText}>Manage</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Story library info */}
          <View style={styles.libraryInfo}>
            <Text style={styles.libraryInfoTitle}>📚 Library Status</Text>
            <Text style={styles.libraryInfoText}>
              {curatedStoriesData.length} curated stories available
            </Text>
            <Text style={styles.libraryInfoText}>Unlimited AI story generation</Text>
          </View>

          {/* Sign out */}
          <TouchableOpacity
            style={styles.signOutButton}
            onPress={handleSignOut}
            activeOpacity={0.8}
          >
            <Text style={styles.signOutText}>Sign Out</Text>
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
    width: 48,
    height: 48,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(45,27,105,0.1)',
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
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginLeft: SPACING.sm,
  },
  headerEmoji: {
    fontSize: 28,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: SPACING.lg,
    paddingBottom: SPACING.xl,
  },
  familyBanner: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.lg,
    padding: SPACING.xl,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: SPACING.xl,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 12,
    elevation: 5,
  },
  familyLabel: {
    fontSize: FONTS.sizes.xs,
    color: 'rgba(255,255,255,0.6)',
    fontWeight: FONTS.weights.medium as any,
  },
  familyName: {
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.white,
    marginTop: 2,
  },
  subBadge: {
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
  },
  subBadgeText: {
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.bold as any,
  },
  sectionTitle: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.md,
    marginTop: SPACING.sm,
  },
  loader: {
    marginVertical: SPACING.xl,
  },
  childCard: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  childCardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  childAvatar: {
    fontSize: 40,
    marginRight: SPACING.md,
  },
  childInfo: {
    flex: 1,
  },
  childName: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  childAge: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    marginTop: 2,
  },
  lastActiveBadge: {
    backgroundColor: COLORS.mint,
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 4,
  },
  lastActiveText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statValue: {
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  statLabel: {
    fontSize: 11,
    color: COLORS.mutedText,
    textAlign: 'center',
    marginTop: 2,
    lineHeight: 16,
  },
  statDivider: {
    width: 1,
    height: 36,
    backgroundColor: COLORS.cream,
  },
  manageVoiceButton: {
    backgroundColor: COLORS.lavender,
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.sm,
    alignItems: 'center',
    minHeight: 44,
    justifyContent: 'center',
  },
  manageVoiceText: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
  },
  addProfileButton: {
    borderWidth: 2,
    borderColor: COLORS.lavender,
    borderStyle: 'dashed',
    borderRadius: RADIUS.lg,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    marginBottom: SPACING.xl,
    minHeight: 64,
    justifyContent: 'center',
  },
  addProfileButtonText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  settingsCard: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.xl,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    minHeight: 60,
  },
  settingInfo: {
    flex: 1,
  },
  settingLabel: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
  },
  settingDesc: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    marginTop: 2,
  },
  settingDivider: {
    height: 1,
    backgroundColor: COLORS.cream,
    marginVertical: SPACING.xs,
  },
  manageSubButton: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.sm,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    minHeight: 36,
    justifyContent: 'center',
  },
  manageSubText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.bold as any,
  },
  libraryInfo: {
    backgroundColor: COLORS.deepIndigo + '15',
    borderRadius: RADIUS.md,
    padding: SPACING.lg,
    marginBottom: SPACING.xl,
  },
  libraryInfoTitle: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.xs,
  },
  libraryInfoText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    marginTop: 4,
  },
  signOutButton: {
    borderWidth: 2,
    borderColor: '#FF6B6B',
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.md,
    alignItems: 'center',
    minHeight: 56,
    justifyContent: 'center',
  },
  signOutText: {
    fontSize: FONTS.sizes.sm,
    color: '#FF6B6B',
    fontWeight: FONTS.weights.bold as any,
  },
  bottomSpacing: {
    height: SPACING.xxl,
  },
});
