import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { login, getMe } from '../api/auth';
import { useAuthStore } from '../store/authStore';
import StarBackground from '../components/StarBackground';

type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  ProfileSelect: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function LoginScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { setAuth } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) {
      setError('Please enter your email and password.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const response = await login(email.trim(), password);
      const { access_token, user } = response.data;
      await setAuth(user, access_token);
      navigation.navigate('ProfileSelect');
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        'Oops! Something went wrong. Please check your details and try again.';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={[COLORS.cream, '#EEE4FF', COLORS.lavender]}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={10} />
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <ScrollView
            contentContainerStyle={styles.scrollContent}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={false}
          >
            {/* Hero Section */}
            <View style={styles.heroSection}>
              <Text style={styles.moonEmoji}>🌙</Text>
              <View style={styles.starsRow}>
                <Text style={styles.starEmoji}>✨</Text>
                <Text style={styles.starEmoji}>⭐</Text>
                <Text style={styles.starEmoji}>✨</Text>
              </View>
              <Text style={styles.appTitle}>Bedtime Stories</Text>
              <Text style={styles.subtitle}>For little dreamers ✨</Text>
            </View>

            {/* Card */}
            <View style={styles.card}>
              {error ? (
                <View style={styles.errorBanner}>
                  <Text style={styles.errorText}>{error}</Text>
                </View>
              ) : null}

              <Text style={styles.inputLabel}>Email</Text>
              <TextInput
                style={styles.input}
                placeholder="your@email.com"
                placeholderTextColor={COLORS.mutedText}
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                returnKeyType="next"
              />

              <Text style={styles.inputLabel}>Password</Text>
              <TextInput
                style={styles.input}
                placeholder="••••••••"
                placeholderTextColor={COLORS.mutedText}
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                returnKeyType="done"
                onSubmitEditing={handleLogin}
              />

              <TouchableOpacity
                style={[styles.loginButton, isLoading && styles.loginButtonDisabled]}
                onPress={handleLogin}
                activeOpacity={0.8}
                disabled={isLoading}
              >
                {isLoading ? (
                  <ActivityIndicator color={COLORS.gold} size="small" />
                ) : (
                  <Text style={styles.loginButtonText}>Let's Begin ✨</Text>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.registerLink}
                onPress={() => navigation.navigate('Register')}
                activeOpacity={0.8}
              >
                <Text style={styles.registerLinkText}>
                  New family?{' '}
                  <Text style={styles.registerLinkBold}>Sign up here</Text>
                </Text>
              </TouchableOpacity>
            </View>

            <View style={styles.bottomSpacing} />
          </ScrollView>
        </KeyboardAvoidingView>
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
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.xl,
  },
  heroSection: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  moonEmoji: {
    fontSize: 72,
    marginBottom: SPACING.xs,
  },
  starsRow: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
  },
  starEmoji: {
    fontSize: 24,
  },
  appTitle: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    textAlign: 'center',
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: FONTS.sizes.md,
    color: COLORS.mutedText,
    textAlign: 'center',
    marginTop: SPACING.xs,
    fontWeight: FONTS.weights.medium as any,
  },
  card: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.lg,
    padding: SPACING.xl,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 16,
    elevation: 6,
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
  inputLabel: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.xs,
    marginLeft: SPACING.xs,
  },
  input: {
    backgroundColor: COLORS.cream,
    borderRadius: RADIUS.md,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    fontSize: FONTS.sizes.md,
    color: COLORS.darkText,
    marginBottom: SPACING.lg,
    borderWidth: 2,
    borderColor: 'transparent',
    minHeight: 56,
  },
  loginButton: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 64,
    marginTop: SPACING.sm,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  loginButtonDisabled: {
    opacity: 0.7,
  },
  loginButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    letterSpacing: 0.5,
  },
  registerLink: {
    alignItems: 'center',
    marginTop: SPACING.lg,
    paddingVertical: SPACING.sm,
    minHeight: 44,
    justifyContent: 'center',
  },
  registerLinkText: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
  },
  registerLinkBold: {
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});
