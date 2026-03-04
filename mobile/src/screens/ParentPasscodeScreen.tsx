import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import * as Haptics from 'expo-haptics';
import * as SecureStore from 'expo-secure-store';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import StarBackground from '../components/StarBackground';

type RootStackParamList = {
  ParentDashboard: undefined;
  ProfileSelect: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

const STORED_PASSCODE_KEY = 'parent_passcode';
const DEFAULT_PASSCODE = '1234';
const PASSCODE_LENGTH = 4;

export default function ParentPasscodeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [entered, setEntered] = useState<string[]>([]);
  const [error, setError] = useState(false);
  const shakeAnim = useRef(new Animated.Value(0)).current;
  const dotAnims = useRef(
    Array.from({ length: PASSCODE_LENGTH }, () => new Animated.Value(1))
  ).current;

  const shake = () => {
    Animated.sequence([
      Animated.timing(shakeAnim, { toValue: 10, duration: 50, useNativeDriver: true }),
      Animated.timing(shakeAnim, { toValue: -10, duration: 50, useNativeDriver: true }),
      Animated.timing(shakeAnim, { toValue: 8, duration: 50, useNativeDriver: true }),
      Animated.timing(shakeAnim, { toValue: -8, duration: 50, useNativeDriver: true }),
      Animated.timing(shakeAnim, { toValue: 0, duration: 50, useNativeDriver: true }),
    ]).start();
  };

  const animateDot = (index: number) => {
    Animated.sequence([
      Animated.timing(dotAnims[index], { toValue: 1.4, duration: 100, useNativeDriver: true }),
      Animated.timing(dotAnims[index], { toValue: 1, duration: 100, useNativeDriver: true }),
    ]).start();
  };

  const handleNumberPress = async (num: string) => {
    if (entered.length >= PASSCODE_LENGTH) return;
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    const newEntered = [...entered, num];
    animateDot(entered.length);
    setEntered(newEntered);
    setError(false);

    if (newEntered.length === PASSCODE_LENGTH) {
      // Check passcode
      const enteredCode = newEntered.join('');
      const storedCode =
        (await SecureStore.getItemAsync(STORED_PASSCODE_KEY)) || DEFAULT_PASSCODE;

      if (enteredCode === storedCode) {
        if (Platform.OS !== 'web') {
          await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        }
        navigation.navigate('ParentDashboard');
      } else {
        if (Platform.OS !== 'web') {
          await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
        }
        setError(true);
        shake();
        setTimeout(() => {
          setEntered([]);
          setError(false);
        }, 1200);
      }
    }
  };

  const handleDelete = async () => {
    if (Platform.OS !== 'web') {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
    setEntered((prev) => prev.slice(0, -1));
    setError(false);
  };

  const keypadRows = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['', '0', 'del'],
  ];

  return (
    <LinearGradient
      colors={[COLORS.deepIndigo, '#1A0D4A', '#0D0820']}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={15} />

        {/* Back button */}
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
          activeOpacity={0.8}
        >
          <Text style={styles.backButtonText}>←</Text>
        </TouchableOpacity>

        <View style={styles.content}>
          {/* Lock icon + title */}
          <View style={styles.titleSection}>
            <Text style={styles.lockEmoji}>🔐</Text>
            <Text style={styles.title}>Parent Mode</Text>
            <Text style={styles.subtitle}>
              {error ? '❌ Incorrect passcode' : 'Enter your passcode'}
            </Text>
          </View>

          {/* Passcode dots */}
          <Animated.View
            style={[styles.dotsRow, { transform: [{ translateX: shakeAnim }] }]}
          >
            {Array.from({ length: PASSCODE_LENGTH }, (_, i) => (
              <Animated.View
                key={i}
                style={[
                  styles.dot,
                  entered.length > i && styles.dotFilled,
                  error && entered.length > i && styles.dotError,
                  { transform: [{ scale: dotAnims[i] }] },
                ]}
              />
            ))}
          </Animated.View>

          {/* Keypad */}
          <View style={styles.keypad}>
            {keypadRows.map((row, rowIdx) => (
              <View key={rowIdx} style={styles.keypadRow}>
                {row.map((key, keyIdx) => {
                  if (key === '') {
                    return <View key={keyIdx} style={styles.keypadEmpty} />;
                  }
                  if (key === 'del') {
                    return (
                      <TouchableOpacity
                        key={keyIdx}
                        style={styles.keypadDeleteButton}
                        onPress={handleDelete}
                        activeOpacity={0.7}
                      >
                        <Text style={styles.keypadDeleteText}>⌫</Text>
                      </TouchableOpacity>
                    );
                  }
                  return (
                    <TouchableOpacity
                      key={keyIdx}
                      style={styles.keypadButton}
                      onPress={() => handleNumberPress(key)}
                      activeOpacity={0.7}
                    >
                      <Text style={styles.keypadButtonText}>{key}</Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            ))}
          </View>

          <Text style={styles.hintText}>Default passcode: 1234</Text>
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
  backButton: {
    marginLeft: SPACING.lg,
    marginTop: SPACING.sm,
    width: 56,
    height: 56,
    borderRadius: RADIUS.round,
    backgroundColor: 'rgba(255,255,255,0.1)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  backButtonText: {
    color: COLORS.white,
    fontSize: FONTS.sizes.lg,
    fontWeight: FONTS.weights.bold as any,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: SPACING.xl,
    paddingBottom: SPACING.xxl,
  },
  titleSection: {
    alignItems: 'center',
    marginBottom: SPACING.xxl,
  },
  lockEmoji: {
    fontSize: 56,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.white,
    marginBottom: SPACING.sm,
  },
  subtitle: {
    fontSize: FONTS.sizes.sm,
    color: 'rgba(255,255,255,0.6)',
    fontWeight: FONTS.weights.medium as any,
  },
  dotsRow: {
    flexDirection: 'row',
    gap: SPACING.lg,
    marginBottom: SPACING.xxl,
  },
  dot: {
    width: 20,
    height: 20,
    borderRadius: RADIUS.round,
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.5)',
    backgroundColor: 'transparent',
  },
  dotFilled: {
    backgroundColor: COLORS.gold,
    borderColor: COLORS.gold,
  },
  dotError: {
    backgroundColor: '#FF6B6B',
    borderColor: '#FF6B6B',
  },
  keypad: {
    width: '100%',
    maxWidth: 300,
    gap: SPACING.sm,
  },
  keypadRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: SPACING.sm,
  },
  keypadButton: {
    flex: 1,
    height: 72,
    borderRadius: RADIUS.md,
    backgroundColor: 'rgba(255,255,255,0.12)',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.15)',
  },
  keypadButtonText: {
    fontSize: FONTS.sizes.lg,
    color: COLORS.white,
    fontWeight: FONTS.weights.bold as any,
  },
  keypadDeleteButton: {
    flex: 1,
    height: 72,
    borderRadius: RADIUS.md,
    backgroundColor: 'rgba(255,255,255,0.06)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  keypadDeleteText: {
    fontSize: FONTS.sizes.md,
    color: 'rgba(255,255,255,0.5)',
  },
  keypadEmpty: {
    flex: 1,
    height: 72,
  },
  hintText: {
    marginTop: SPACING.xl,
    fontSize: FONTS.sizes.xs,
    color: 'rgba(255,255,255,0.3)',
    fontWeight: FONTS.weights.medium as any,
  },
});
