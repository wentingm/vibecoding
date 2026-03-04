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
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { register, getMe } from '../api/auth';
import { useAuthStore } from '../store/authStore';
import StarBackground from '../components/StarBackground';

type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  ProfileSelect: undefined;
};

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function RegisterScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { setAuth } = useAuthStore();
  const [familyName, setFamilyName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async () => {
    if (!familyName.trim() || !email.trim() || !password.trim()) {
      setError('Please fill in all fields to get started!');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const response = await register(email.trim(), password, familyName.trim());
      const { access_token, user } = response.data;
      await setAuth(user, access_token);
      navigation.navigate('ProfileSelect');
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        'Could not create your account. Please try again.';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={[COLORS.cream, '#FFE8F4', COLORS.rose]}
      style={styles.gradient}
      start={{ x: 0, y: 0 }}
      end={{ x: 0, y: 1 }}
    >
      <SafeAreaView style={styles.safe}>
        <StarBackground count={8} />
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <ScrollView
            contentContainerStyle={styles.scrollContent}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={false}
          >
            {/* Back button */}
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => navigation.goBack()}
              activeOpacity={0.8}
            >
              <Text style={styles.backButtonText}>← Back</Text>
            </TouchableOpacity>

            {/* Hero */}
            <View style={styles.heroSection}>
              <Text style={styles.heroEmoji}>🏠</Text>
              <Text style={styles.heroTitle}>Create Your{'\n'}Family Account</Text>
              <Text style={styles.heroSubtitle}>Start your bedtime adventure</Text>
            </View>

            {/* Card */}
            <View style={styles.card}>
              {error ? (
                <View style={styles.errorBanner}>
                  <Text style={styles.errorText}>{error}</Text>
                </View>
              ) : null}

              <Text style={styles.inputLabel}>Family Name</Text>
              <TextInput
                style={styles.input}
                placeholder="e.g. The Smiths"
                placeholderTextColor={COLORS.mutedText}
                value={familyName}
                onChangeText={setFamilyName}
                autoCapitalize="words"
                returnKeyType="next"
              />

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
                placeholder="At least 6 characters"
                placeholderTextColor={COLORS.mutedText}
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                returnKeyType="done"
                onSubmitEditing={handleRegister}
              />

              <TouchableOpacity
                style={[styles.registerButton, isLoading && styles.buttonDisabled]}
                onPress={handleRegister}
                activeOpacity={0.8}
                disabled={isLoading}
              >
                {isLoading ? (
                  <ActivityIndicator color={COLORS.gold} size="small" />
                ) : (
                  <Text style={styles.registerButtonText}>Create Account 🌟</Text>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.loginLink}
                onPress={() => navigation.navigate('Login')}
                activeOpacity={0.8}
              >
                <Text style={styles.loginLinkText}>
                  Already have an account?{' '}
                  <Text style={styles.loginLinkBold}>Sign in</Text>
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
    paddingTop: SPACING.md,
  },
  backButton: {
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.xs,
    alignSelf: 'flex-start',
    minHeight: 44,
    justifyContent: 'center',
  },
  backButtonText: {
    fontSize: FONTS.sizes.md,
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.medium as any,
  },
  heroSection: {
    alignItems: 'center',
    marginVertical: SPACING.xl,
  },
  heroEmoji: {
    fontSize: 64,
    marginBottom: SPACING.sm,
  },
  heroTitle: {
    fontSize: FONTS.sizes.xl,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
    textAlign: 'center',
    lineHeight: 44,
  },
  heroSubtitle: {
    fontSize: FONTS.sizes.sm,
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
  registerButton: {
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
  buttonDisabled: {
    opacity: 0.7,
  },
  registerButtonText: {
    color: COLORS.gold,
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    letterSpacing: 0.5,
  },
  loginLink: {
    alignItems: 'center',
    marginTop: SPACING.lg,
    paddingVertical: SPACING.sm,
    minHeight: 44,
    justifyContent: 'center',
  },
  loginLinkText: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
  },
  loginLinkBold: {
    color: COLORS.deepIndigo,
    fontWeight: FONTS.weights.bold as any,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});
