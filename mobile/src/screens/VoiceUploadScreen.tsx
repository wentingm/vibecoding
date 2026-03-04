import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import * as DocumentPicker from 'expo-document-picker';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { apiClient } from '../api/client';

type VoiceLabel = 'Mom' | 'Dad';

interface VoiceStatus {
  mom: boolean;
  dad: boolean;
}

export default function VoiceUploadScreen() {
  const navigation = useNavigation();
  const [uploading, setUploading] = useState<VoiceLabel | null>(null);
  const [voiceStatus, setVoiceStatus] = useState<VoiceStatus>({ mom: false, dad: false });

  useEffect(() => {
    loadVoiceStatus();
  }, []);

  const loadVoiceStatus = async () => {
    try {
      const { data } = await apiClient.get('/voices/my-voices');
      setVoiceStatus({
        mom: !!data.mom_voice_id,
        dad: !!data.dad_voice_id,
      });
    } catch {}
  };

  const handleUpload = async (label: VoiceLabel) => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['audio/*'],
        copyToCacheDirectory: true,
      });

      if (result.canceled) return;

      const file = result.assets[0];
      setUploading(label);

      const formData = new FormData();
      formData.append('label', label);
      formData.append('file', {
        uri: file.uri,
        name: file.name,
        type: file.mimeType || 'audio/m4a',
      } as any);

      await apiClient.post('/voices/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      });

      setVoiceStatus(prev => ({ ...prev, [label.toLowerCase()]: true }));
      Alert.alert(
        '🎉 Voice Cloned!',
        `${label}'s voice has been cloned successfully. New stories will be narrated in your voice!`,
        [{ text: 'Awesome!' }]
      );
    } catch (e: any) {
      Alert.alert('Upload Failed', e?.response?.data?.detail || 'Please try again with a longer recording (30+ seconds).');
    } finally {
      setUploading(null);
    }
  };

  const VoiceCard = ({ label, emoji }: { label: VoiceLabel; emoji: string }) => {
    const isReady = voiceStatus[label.toLowerCase() as keyof VoiceStatus];
    const isUploading = uploading === label;

    return (
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardEmoji}>{emoji}</Text>
          <View style={styles.cardInfo}>
            <Text style={styles.cardTitle}>{label}'s Voice</Text>
            <Text style={[styles.cardStatus, { color: isReady ? '#4CAF50' : COLORS.mutedText }]}>
              {isReady ? '✓ Voice ready' : 'Not set up yet'}
            </Text>
          </View>
          {isReady && <Text style={styles.readyBadge}>✓</Text>}
        </View>

        <Text style={styles.cardHint}>
          Record yourself reading a bedtime story or any passage (30+ seconds) using your phone's Voice Memos app, then upload it here.
        </Text>

        <TouchableOpacity
          style={[styles.uploadButton, isReady && styles.uploadButtonUpdate]}
          onPress={() => handleUpload(label)}
          disabled={isUploading}
          activeOpacity={0.8}
        >
          {isUploading ? (
            <View style={styles.uploadingRow}>
              <ActivityIndicator color={COLORS.white} size="small" />
              <Text style={styles.uploadButtonText}>  Cloning voice...</Text>
            </View>
          ) : (
            <Text style={styles.uploadButtonText}>
              {isReady ? '🔄 Re-upload Voice' : '🎙 Upload Voice Recording'}
            </Text>
          )}
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <LinearGradient colors={[COLORS.cream, '#EEF2FF']} style={styles.gradient}>
      <SafeAreaView style={styles.safe}>
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
            activeOpacity={0.8}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Parent Voices</Text>
          <Text style={styles.headerEmoji}>🎙</Text>
        </View>

        <View style={styles.content}>
          <Text style={styles.subtitle}>
            Clone your voice so your children hear you narrate their bedtime stories — even when you're not there.
          </Text>

          <VoiceCard label="Mom" emoji="👩" />
          <VoiceCard label="Dad" emoji="👨" />

          <View style={styles.tipBox}>
            <Text style={styles.tipTitle}>💡 Tips for best results</Text>
            <Text style={styles.tipText}>• Record in a quiet room</Text>
            <Text style={styles.tipText}>• Speak naturally and clearly</Text>
            <Text style={styles.tipText}>• At least 1 minute of audio works best</Text>
            <Text style={styles.tipText}>• Use iPhone Voice Memos app to record</Text>
          </View>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: { flex: 1 },
  safe: { flex: 1 },
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
  headerEmoji: { fontSize: 28 },
  content: {
    flex: 1,
    paddingHorizontal: SPACING.lg,
  },
  subtitle: {
    fontSize: FONTS.sizes.sm,
    color: COLORS.mutedText,
    lineHeight: 22,
    marginBottom: SPACING.xl,
  },
  card: {
    backgroundColor: COLORS.white,
    borderRadius: RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    shadowColor: COLORS.deepIndigo,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  cardEmoji: { fontSize: 36, marginRight: SPACING.md },
  cardInfo: { flex: 1 },
  cardTitle: {
    fontSize: FONTS.sizes.md,
    fontWeight: FONTS.weights.heavy as any,
    color: COLORS.deepIndigo,
  },
  cardStatus: {
    fontSize: FONTS.sizes.xs,
    marginTop: 2,
  },
  readyBadge: {
    fontSize: 24,
    color: '#4CAF50',
  },
  cardHint: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    lineHeight: 18,
    marginBottom: SPACING.md,
  },
  uploadButton: {
    backgroundColor: COLORS.deepIndigo,
    borderRadius: RADIUS.md,
    paddingVertical: SPACING.md,
    alignItems: 'center',
    minHeight: 52,
    justifyContent: 'center',
  },
  uploadButtonUpdate: {
    backgroundColor: COLORS.lavender,
  },
  uploadButtonText: {
    color: COLORS.white,
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
  },
  uploadingRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  tipBox: {
    backgroundColor: COLORS.deepIndigo + '10',
    borderRadius: RADIUS.md,
    padding: SPACING.lg,
    marginTop: SPACING.sm,
  },
  tipTitle: {
    fontSize: FONTS.sizes.sm,
    fontWeight: FONTS.weights.bold as any,
    color: COLORS.deepIndigo,
    marginBottom: SPACING.sm,
  },
  tipText: {
    fontSize: FONTS.sizes.xs,
    color: COLORS.mutedText,
    lineHeight: 22,
  },
});
