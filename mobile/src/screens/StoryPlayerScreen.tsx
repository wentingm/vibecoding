import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  Animated,
  Platform,
  Image,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Audio, isAudioAvailable } from '../hooks/useAudio';
import * as Speech from 'expo-speech';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { Story } from '../types';

const { width, height } = Dimensions.get('window');

type RootStackParamList = {
  StoryPlayer: { story: Story };
  SleepMode: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
type RoutePropType = RouteProp<RootStackParamList, 'StoryPlayer'>;

const AUTO_ADVANCE_SECONDS = 15;

// Pick the best available iOS voice (premium > enhanced > default)
async function getBestVoice(): Promise<string | undefined> {
  try {
    const voices = await Speech.getAvailableVoicesAsync();
    const enVoices = voices.filter(v => v.language.startsWith('en'));
    // Prefer female voices with premium/enhanced quality — more soothing for bedtime
    const preferredNames = ['Ava', 'Samantha', 'Zoe', 'Karen', 'Moira'];
    for (const name of preferredNames) {
      const premium = enVoices.find(v => v.identifier.toLowerCase().includes(name.toLowerCase()) && v.quality === 'Enhanced');
      if (premium) {
        console.log('[Voice] Using premium:', premium.identifier);
        return premium.identifier;
      }
    }
    const anyEnhanced = enVoices.find(v => v.quality === 'Enhanced');
    if (anyEnhanced) {
      console.log('[Voice] Using enhanced:', anyEnhanced.identifier);
      return anyEnhanced.identifier;
    }
    const anyEn = enVoices[0];
    console.log('[Voice] Using default:', anyEn?.identifier);
    return anyEn?.identifier;
  } catch {
    return undefined;
  }
}

export default function StoryPlayerScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<RoutePropType>();
  const { story } = route.params;

  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState(AUTO_ADVANCE_SECONDS);

  const slideAnim = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Ken Burns parallax
  const kbScale = useRef(new Animated.Value(1)).current;
  const kbX     = useRef(new Animated.Value(0)).current;
  const kbY     = useRef(new Animated.Value(0)).current;
  const kbAnim  = useRef<Animated.CompositeAnimation | null>(null);

  // Ken Burns directions cycle — zoom + slow drift in alternating directions
  const KB_DIRECTIONS = [
    { x: 12, y: 6  },
    { x: -12, y: -6 },
    { x: 6,  y: -12 },
    { x: -6, y: 12  },
    { x: 0,  y: -14 },
    { x: 0,  y: 14  },
  ];

  const currentPage = story.pages[currentPageIndex];
  const totalPages = story.pages.length;
  const isLastPage = currentPageIndex === totalPages - 1;

  const bgColor = (currentPage as any)?.bg_color || COLORS.deepIndigo;
  const pageEmoji = (currentPage as any)?.emoji || '📖';

  // Cleanup audio on unmount
  useEffect(() => {
    return () => {
      if (sound) sound.unloadAsync();
      Speech.stop();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [sound]);

  // Ken Burns animation — restart on every page change
  useEffect(() => {
    if (kbAnim.current) kbAnim.current.stop();
    kbScale.setValue(1);
    kbX.setValue(0);
    kbY.setValue(0);

    const dir = KB_DIRECTIONS[currentPageIndex % KB_DIRECTIONS.length];
    kbAnim.current = Animated.parallel([
      Animated.timing(kbScale, { toValue: 1.14, duration: 22000, useNativeDriver: true }),
      Animated.timing(kbX,     { toValue: dir.x, duration: 22000, useNativeDriver: true }),
      Animated.timing(kbY,     { toValue: dir.y, duration: 22000, useNativeDriver: true }),
    ]);
    kbAnim.current.start();
    return () => { kbAnim.current?.stop(); };
  }, [currentPageIndex]);

  // Play audio or TTS for the current page
  useEffect(() => {
    const loadAudio = async () => {
      // Stop any previous speech
      Speech.stop();
      if (sound) {
        await sound.unloadAsync();
        setSound(null);
      }

      const audioUrl = currentPage?.audio_url;
      const pageText = currentPage?.text;

      // Try expo-av first (native build), fall back to expo-speech (Expo Go)
      if (audioUrl && isAudioAvailable) {
        try {
          await Audio.setAudioModeAsync({
            playsInSilentModeIOS: true,
            allowsRecordingIOS: false,
            staysActiveInBackground: true,
          });
          const { sound: newSound } = await Audio.Sound.createAsync(
            { uri: audioUrl },
            { shouldPlay: true, rate: 0.88, shouldCorrectPitch: true, volume: 1.0 }
          );
          setSound(newSound);
          setIsPlaying(true);
          newSound.setOnPlaybackStatusUpdate((status: any) => {
            if (status.isLoaded && status.didJustFinish) {
              setIsPlaying(false);
              handleAutoAdvance();
            }
          });
          return;
        } catch (e) {
          console.log('[StoryPlayer] expo-av error:', e);
        }
      }

      // Fall back to expo-speech (works in Expo Go)
      if (pageText) {
        setIsPlaying(true);
        const bestVoice = await getBestVoice();
        Speech.speak(pageText, {
          rate: 0.62,
          pitch: 1.0,
          voice: bestVoice,
          onDone: () => {
            setIsPlaying(false);
            handleAutoAdvance();
          },
          onError: () => {
            setIsPlaying(false);
            startAutoAdvanceTimer();
          },
        });
      } else {
        startAutoAdvanceTimer();
      }
    };
    loadAudio();
  }, [currentPageIndex]);

  const startAutoAdvanceTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setAutoAdvanceTimer(AUTO_ADVANCE_SECONDS);
    timerRef.current = setInterval(() => {
      setAutoAdvanceTimer((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current!);
          handleAutoAdvance();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleAutoAdvance = () => {
    if (isLastPage) {
      setTimeout(() => {
        navigation.navigate('SleepMode');
      }, 3000);
    } else {
      goToNextPage();
    }
  };

  const animatePageTransition = (direction: 'left' | 'right', callback: () => void) => {
    if (timerRef.current) clearInterval(timerRef.current);

    // Slide out
    Animated.parallel([
      Animated.timing(slideAnim, {
        toValue: direction === 'left' ? -width : width,
        duration: 250,
        useNativeDriver: true,
      }),
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start(() => {
      slideAnim.setValue(direction === 'left' ? width : -width);
      callback();
      // Slide in
      Animated.parallel([
        Animated.spring(slideAnim, {
          toValue: 0,
          useNativeDriver: true,
          tension: 80,
          friction: 12,
        }),
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 250,
          useNativeDriver: true,
        }),
      ]).start();
    });
  };

  const goToNextPage = () => {
    if (currentPageIndex < totalPages - 1) {
      animatePageTransition('left', () => {
        setCurrentPageIndex((prev) => prev + 1);
      });
    }
  };

  const goToPrevPage = () => {
    if (currentPageIndex > 0) {
      animatePageTransition('right', () => {
        setCurrentPageIndex((prev) => prev - 1);
      });
    }
  };

  const togglePlayPause = async () => {
    if (sound) {
      const status = await sound.getStatusAsync();
      if (status.isLoaded) {
        if (status.isPlaying) {
          await sound.pauseAsync();
          setIsPlaying(false);
        } else {
          await sound.playAsync();
          setIsPlaying(true);
        }
      }
    }
  };

  const handleClose = () => {
    if (sound) sound.unloadAsync();
    Speech.stop();
    if (timerRef.current) clearInterval(timerRef.current);
    navigation.goBack();
  };

  return (
    <View style={[styles.container, { backgroundColor: bgColor }]}>
      <SafeAreaView style={styles.safe}>
        {/* Close button */}
        <TouchableOpacity
          style={styles.closeButton}
          onPress={handleClose}
          activeOpacity={0.8}
        >
          <Text style={styles.closeButtonText}>✕</Text>
        </TouchableOpacity>

        {/* Story title */}
        <View style={styles.titleBar}>
          <Text style={styles.storyTitle} numberOfLines={1}>
            {story.title}
          </Text>
        </View>

        {/* Main illustration + text area */}
        <Animated.View
          style={[
            styles.pageContainer,
            {
              transform: [{ translateX: slideAnim }],
              opacity: fadeAnim,
            },
          ]}
        >
          {/* Illustration panel */}
          <View style={styles.illustrationPanel}>
            {currentPage?.illustration_url ? (
              <Animated.View
                style={[
                  styles.parallaxWrapper,
                  { transform: [{ scale: kbScale }, { translateX: kbX }, { translateY: kbY }] },
                ]}
              >
                <Image
                  source={{ uri: currentPage.illustration_url }}
                  style={styles.illustrationImage}
                  resizeMode="cover"
                />
              </Animated.View>
            ) : (
              <Text style={styles.illustrationEmoji}>{pageEmoji}</Text>
            )}
            {/* Auto-advance progress arc */}
            <View style={styles.timerIndicator}>
              <Text style={styles.timerText}>{autoAdvanceTimer}s</Text>
            </View>
          </View>

          {/* Text panel */}
          <View style={styles.textPanel}>
            <ScrollView
              contentContainerStyle={styles.textScroll}
              showsVerticalScrollIndicator={false}
            >
              <Text style={styles.pageText}>{currentPage?.text}</Text>
            </ScrollView>
          </View>
        </Animated.View>

        {/* Bottom controls */}
        <View style={styles.bottomControls}>
          {/* Prev button */}
          <TouchableOpacity
            style={[styles.navButton, currentPageIndex === 0 && styles.navButtonDisabled]}
            onPress={goToPrevPage}
            activeOpacity={0.8}
            disabled={currentPageIndex === 0}
          >
            <Text style={styles.navButtonText}>←</Text>
          </TouchableOpacity>

          {/* Progress dots + play/pause */}
          <View style={styles.centerControls}>
            {/* Progress dots */}
            <View style={styles.progressDots}>
              {story.pages.map((_, i) => (
                <View
                  key={i}
                  style={[
                    styles.progressDot,
                    i === currentPageIndex && styles.progressDotActive,
                    i < currentPageIndex && styles.progressDotDone,
                  ]}
                />
              ))}
            </View>

            {/* Play/Pause */}
            <TouchableOpacity
              style={styles.playButton}
              onPress={togglePlayPause}
              activeOpacity={0.8}
            >
              <Text style={styles.playButtonText}>{isPlaying ? '⏸' : '▶'}</Text>
            </TouchableOpacity>
          </View>

          {/* Next button */}
          <TouchableOpacity
            style={[styles.navButton, isLastPage && styles.navButtonSleep]}
            onPress={isLastPage ? () => navigation.navigate('SleepMode') : goToNextPage}
            activeOpacity={0.8}
          >
            <Text style={styles.navButtonText}>{isLastPage ? '🌙' : '→'}</Text>
          </TouchableOpacity>
        </View>

        {/* Page indicator */}
        <Text style={styles.pageIndicator}>
          Page {currentPageIndex + 1} of {totalPages}
        </Text>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safe: {
    flex: 1,
  },
  closeButton: {
    position: 'absolute',
    top: 56,
    left: SPACING.lg,
    zIndex: 10,
    width: 44,
    height: 44,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(0,0,0,0.3)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  closeButtonText: {
    color: COLORS.white,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.bold as any,
  },
  titleBar: {
    paddingTop: SPACING.sm,
    paddingHorizontal: SPACING.xxl + SPACING.lg,
    paddingBottom: SPACING.sm,
    alignItems: 'center',
  },
  storyTitle: {
    fontSize: FONTS.sizes.sm,
    color: 'rgba(255,255,255,0.7)',
    fontWeight: FONTS.weights.medium as any,
    textAlign: 'center',
  },
  pageContainer: {
    flex: 1,
  },
  illustrationPanel: {
    height: height * 0.45,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    overflow: 'hidden',
  },
  parallaxWrapper: {
    width: '100%',
    height: '100%',
  },
  illustrationImage: {
    width: '100%',
    height: '100%',
  },
  illustrationEmoji: {
    fontSize: 120,
  },
  timerIndicator: {
    position: 'absolute',
    bottom: SPACING.md,
    right: SPACING.lg,
    backgroundColor: 'rgba(0,0,0,0.3)',
    borderRadius: RADIUS.round,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 4,
  },
  timerText: {
    color: 'rgba(255,255,255,0.6)',
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.medium as any,
  },
  textPanel: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.35)',
    borderTopLeftRadius: RADIUS.xl,
    borderTopRightRadius: RADIUS.xl,
    paddingHorizontal: SPACING.xl,
    paddingTop: SPACING.md,
    paddingBottom: SPACING.sm,
  },
  textScroll: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingVertical: SPACING.md,
  },
  pageText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.white,
    lineHeight: 30,
    textAlign: 'center',
    fontWeight: FONTS.weights.medium as any,
    letterSpacing: 0.3,
  },
  bottomControls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    backgroundColor: 'rgba(0,0,0,0.35)',
  },
  navButton: {
    width: 64,
    height: 64,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.3)',
  },
  navButtonDisabled: {
    opacity: 0.3,
  },
  navButtonSleep: {
    backgroundColor: COLORS.deepIndigo,
    borderColor: COLORS.lavender,
  },
  navButtonText: {
    color: COLORS.white,
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.bold as any,
  },
  centerControls: {
    alignItems: 'center',
    gap: SPACING.sm,
  },
  progressDots: {
    flexDirection: 'row',
    gap: SPACING.xs,
    alignItems: 'center',
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.3)',
  },
  progressDotActive: {
    backgroundColor: COLORS.gold,
    width: 20,
  },
  progressDotDone: {
    backgroundColor: 'rgba(255,255,255,0.6)',
  },
  playButton: {
    width: 56,
    height: 56,
    borderRadius: RADIUS.round,
    backgroundColor: COLORS.gold,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: COLORS.gold,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
    elevation: 4,
  },
  playButtonText: {
    fontSize: FONTS.sizes.md,
  },
  pageIndicator: {
    textAlign: 'center',
    color: 'rgba(255,255,255,0.5)',
    fontSize: FONTS.sizes.xs,
    paddingBottom: SPACING.sm,
    backgroundColor: 'rgba(0,0,0,0.35)',
  },
});
