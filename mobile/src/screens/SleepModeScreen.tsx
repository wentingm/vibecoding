import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Audio, isAudioAvailable } from '../hooks/useAudio';

let Brightness: any = null;
try { Brightness = require('expo-brightness'); } catch {}

let activateKeepAwakeAsync: any = null;
let deactivateKeepAwake: any = null;
try {
  const ka = require('expo-keep-awake');
  activateKeepAwakeAsync = ka.activateKeepAwakeAsync;
  deactivateKeepAwake = ka.deactivateKeepAwake;
} catch {}
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';

const { width, height } = Dimensions.get('window');

type RootStackParamList = {
  ProfileSelect: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

const TIMER_OPTIONS = [
  { label: '5 min', seconds: 300 },
  { label: '10 min', seconds: 600 },
  { label: '15 min', seconds: 900 },
  { label: '30 min', seconds: 1800 },
];

interface FallingStarProps {
  index: number;
}

function FallingStar({ index }: FallingStarProps) {
  const opacity = useRef(new Animated.Value(0)).current;
  const stars = ['⭐', '✨', '💫'];
  const emoji = stars[index % stars.length];
  const left = 10 + (index * 73) % 80;
  const delay = (index * 600) % 3000;
  const size = 12 + (index * 7) % 14;

  useEffect(() => {
    const animate = () => {
      Animated.sequence([
        Animated.delay(delay),
        Animated.timing(opacity, { toValue: 0.7, duration: 1500, useNativeDriver: true }),
        Animated.timing(opacity, { toValue: 0, duration: 1500, useNativeDriver: true }),
        Animated.delay(Math.random() * 2000),
      ]).start(() => animate());
    };
    animate();
  }, []);

  return (
    <Animated.Text
      style={[
        styles.fallingStar,
        {
          left: `${left}%` as any,
          top: 60 + (index * 100) % (height * 0.6),
          opacity,
          fontSize: size,
        },
      ]}
    >
      {emoji}
    </Animated.Text>
  );
}

export default function SleepModeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [showTimers, setShowTimers] = useState(true);
  const [selectedTimer, setSelectedTimer] = useState(TIMER_OPTIONS[1]);
  const [secondsLeft, setSecondsLeft] = useState<number | null>(null);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [sound, setSound] = useState<any>(null);

  const bgAnim = useRef(new Animated.Value(0)).current;
  const moonScale = useRef(new Animated.Value(1)).current;
  const textOpacity = useRef(new Animated.Value(0)).current;
  const timerOpacity = useRef(new Animated.Value(1)).current;
  const timerHideRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    // Keep screen on
    activateKeepAwakeAsync?.();
    // Dim screen
    dimScreen();
    // Start animations
    startAnimations();
    // Hide timer panel after 10 seconds
    timerHideRef.current = setTimeout(() => hideTimerPanel(), 10000);

    return () => {
      deactivateKeepAwake?.();
      restoreBrightness();
      if (sound) sound.unloadAsync();
      if (timerHideRef.current) clearTimeout(timerHideRef.current);
      if (countdownRef.current) clearInterval(countdownRef.current);
    };
  }, []);

  const dimScreen = async () => {
    try {
      if (!Brightness) return;
      const { status } = await Brightness.requestPermissionsAsync();
      if (status === 'granted') await Brightness.setSystemBrightnessAsync(0.05);
    } catch {}
  };

  const restoreBrightness = async () => {
    try {
      if (Brightness) await Brightness.setSystemBrightnessAsync(0.5);
    } catch {}
  };

  const startAnimations = () => {
    // Background fade to black
    Animated.timing(bgAnim, {
      toValue: 1,
      duration: 30000,
      useNativeDriver: false,
    }).start();

    // Moon pulse animation
    const pulseMoon = () => {
      Animated.sequence([
        Animated.timing(moonScale, { toValue: 1.1, duration: 2500, useNativeDriver: true }),
        Animated.timing(moonScale, { toValue: 1.0, duration: 2500, useNativeDriver: true }),
      ]).start(() => pulseMoon());
    };
    pulseMoon();

    // "Sweet dreams" text fade in and out
    Animated.sequence([
      Animated.delay(2000),
      Animated.timing(textOpacity, { toValue: 1, duration: 3000, useNativeDriver: true }),
      Animated.delay(5000),
      Animated.timing(textOpacity, { toValue: 0, duration: 3000, useNativeDriver: true }),
    ]).start();
  };

  const hideTimerPanel = () => {
    Animated.timing(timerOpacity, {
      toValue: 0,
      duration: 1000,
      useNativeDriver: true,
    }).start(() => setShowTimers(false));
  };

  const showTimerPanel = () => {
    setShowTimers(true);
    Animated.timing(timerOpacity, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
    // Re-hide after 10 seconds
    if (timerHideRef.current) clearTimeout(timerHideRef.current);
    timerHideRef.current = setTimeout(() => hideTimerPanel(), 10000);
  };

  const startTimer = () => {
    if (countdownRef.current) clearInterval(countdownRef.current);
    setSecondsLeft(selectedTimer.seconds);
    setIsTimerRunning(true);
    hideTimerPanel();

    countdownRef.current = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev === null || prev <= 1) {
          clearInterval(countdownRef.current!);
          setIsTimerRunning(false);
          // Timer expired - go back to home
          setTimeout(() => navigation.navigate('ProfileSelect'), 2000);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleScreenTap = () => {
    showTimerPanel();
  };

  const bgColor = bgAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [COLORS.deepIndigo, '#000000'],
  });

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <Animated.View style={[styles.container, { backgroundColor: bgColor }]}>
      <TouchableOpacity
        style={StyleSheet.absoluteFill}
        onPress={handleScreenTap}
        activeOpacity={1}
      >
        {/* Stars */}
        {Array.from({ length: 10 }, (_, i) => (
          <FallingStar key={i} index={i} />
        ))}

        <SafeAreaView style={styles.safe}>
          {/* Timer display if running */}
          {isTimerRunning && secondsLeft !== null && (
            <View style={styles.timerDisplay}>
              <Text style={styles.timerDisplayText}>{formatTime(secondsLeft)}</Text>
            </View>
          )}

          {/* Moon */}
          <View style={styles.moonContainer}>
            <Animated.Text
              style={[styles.moonEmoji, { transform: [{ scale: moonScale }] }]}
            >
              🌙
            </Animated.Text>
            <Animated.Text style={[styles.sweetDreamsText, { opacity: textOpacity }]}>
              Sweet dreams...
            </Animated.Text>
          </View>

          {/* Timer options */}
          {showTimers && (
            <Animated.View style={[styles.timerPanel, { opacity: timerOpacity }]}>
              <Text style={styles.timerPanelTitle}>Sleep timer</Text>
              <View style={styles.timerOptions}>
                {TIMER_OPTIONS.map((option) => (
                  <TouchableOpacity
                    key={option.seconds}
                    style={[
                      styles.timerOption,
                      selectedTimer.seconds === option.seconds && styles.timerOptionSelected,
                    ]}
                    onPress={(e) => {
                      e.stopPropagation();
                      setSelectedTimer(option);
                    }}
                    activeOpacity={0.8}
                  >
                    <Text
                      style={[
                        styles.timerOptionText,
                        selectedTimer.seconds === option.seconds &&
                          styles.timerOptionTextSelected,
                      ]}
                    >
                      {option.label}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
              <TouchableOpacity
                style={styles.startTimerButton}
                onPress={(e) => {
                  e.stopPropagation();
                  startTimer();
                }}
                activeOpacity={0.8}
              >
                <Text style={styles.startTimerText}>Start Timer</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.exitButton}
                onPress={(e) => {
                  e.stopPropagation();
                  navigation.navigate('ProfileSelect');
                }}
                activeOpacity={0.8}
              >
                <Text style={styles.exitButtonText}>Exit to Home</Text>
              </TouchableOpacity>
            </Animated.View>
          )}
        </SafeAreaView>
      </TouchableOpacity>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safe: {
    flex: 1,
    alignItems: 'center',
  },
  fallingStar: {
    position: 'absolute',
  },
  timerDisplay: {
    marginTop: SPACING.lg,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: RADIUS.md,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
  },
  timerDisplayText: {
    color: 'rgba(255,255,255,0.5)',
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.medium as any,
    fontVariant: ['tabular-nums'],
  },
  moonContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  moonEmoji: {
    fontSize: 100,
    marginBottom: SPACING.xl,
  },
  sweetDreamsText: {
    fontSize: FONTS.sizes.lg,
    color: 'rgba(255,255,255,0.6)',
    fontWeight: FONTS.weights.medium as any,
    letterSpacing: 1,
    fontStyle: 'italic',
  },
  timerPanel: {
    width: width - SPACING.xl * 2,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: RADIUS.lg,
    padding: SPACING.xl,
    marginBottom: SPACING.xxl,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.15)',
  },
  timerPanelTitle: {
    fontSize: FONTS.sizes.md,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: FONTS.weights.bold as any,
    marginBottom: SPACING.md,
    letterSpacing: 0.5,
  },
  timerOptions: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  timerOption: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.2)',
    minHeight: 44,
    justifyContent: 'center',
  },
  timerOptionSelected: {
    backgroundColor: COLORS.lavender,
    borderColor: COLORS.lavender,
  },
  timerOptionText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.medium as any,
  },
  timerOptionTextSelected: {
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  startTimerButton: {
    backgroundColor: COLORS.gold,
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.xl,
    width: '100%',
    alignItems: 'center',
    minHeight: 52,
    marginBottom: SPACING.sm,
  },
  startTimerText: {
    color: COLORS.deepIndigo,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
  },
  exitButton: {
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.lg,
    minHeight: 44,
    justifyContent: 'center',
  },
  exitButtonText: {
    color: 'rgba(255,255,255,0.5)',
    fontSize: FONTS.sizes.xs,
    fontWeight: FONTS.weights.medium as any,
  },
});
