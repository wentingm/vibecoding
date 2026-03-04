import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import * as DocumentPicker from 'expo-document-picker';
import { COLORS, FONTS, SPACING, RADIUS } from '../constants/theme';
import { apiClient } from '../api/client';

// Audio recording — only available in native builds
let Audio: any = null;
try { Audio = require('expo-av').Audio; } catch {}
const canRecord = !!Audio;

type VoiceLabel = 'Mom' | 'Dad';
type RecordingState = 'idle' | 'recording' | 'recorded';

interface VoiceStatus {
  mom: boolean;
  dad: boolean;
}

export default function VoiceUploadScreen() {
  const navigation = useNavigation();
  const [uploading, setUploading] = useState<VoiceLabel | null>(null);
  const [voiceStatus, setVoiceStatus] = useState<VoiceStatus>({ mom: false, dad: false });
  const [recordingState, setRecordingState] = useState<RecordingState>('idle');
  const [recordingLabel, setRecordingLabel] = useState<VoiceLabel | null>(null);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const recordingRef = useRef<any>(null);
  const timerRef = useRef<any>(null);

  useEffect(() => {
    loadVoiceStatus();
    return () => {
      stopRecordingCleanup();
    };
  }, []);

  const loadVoiceStatus = async () => {
    try {
      const { data } = await apiClient.get('/voices/my-voices');
      setVoiceStatus({ mom: !!data.mom_voice_id, dad: !!data.dad_voice_id });
    } catch {}
  };

  const stopRecordingCleanup = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (recordingRef.current) {
      try { recordingRef.current.stopAndUnloadAsync(); } catch {}
    }
  };

  const startRecording = async (label: VoiceLabel) => {
    if (!canRecord) {
      Alert.alert(
        'Not Available',
        'In-app recording requires the native app build. Use "Upload from Files" instead — record with Voice Memos, then upload here.',
        [{ text: 'OK' }]
      );
      return;
    }
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      recordingRef.current = recording;
      setRecordingLabel(label);
      setRecordingState('recording');
      setRecordingSeconds(0);
      timerRef.current = setInterval(() => setRecordingSeconds(s => s + 1), 1000);
    } catch (e) {
      Alert.alert('Error', 'Could not start recording. Please check microphone permissions.');
    }
  };

  const stopRecording = async () => {
    if (!recordingRef.current) return;
    clearInterval(timerRef.current);
    try {
      await recordingRef.current.stopAndUnloadAsync();
      setRecordingState('recorded');
    } catch {}
  };

  const uploadRecording = async () => {
    if (!recordingRef.current || !recordingLabel) return;
    const uri = recordingRef.current.getURI();
    if (!uri) return;
    await uploadAudio(recordingLabel, uri, 'recording.m4a', 'audio/m4a');
    recordingRef.current = null;
    setRecordingState('idle');
    setRecordingLabel(null);
  };

  const discardRecording = () => {
    if (recordingRef.current) {
      try { recordingRef.current.stopAndUnloadAsync(); } catch {}
      recordingRef.current = null;
    }
    setRecordingState('idle');
    setRecordingLabel(null);
    setRecordingSeconds(0);
  };

  const handleUploadFile = async (label: VoiceLabel) => {
    try {
      const result = await DocumentPicker.getDocumentAsync({ type: ['audio/*'], copyToCacheDirectory: true });
      if (result.canceled) return;
      const file = result.assets[0];
      await uploadAudio(label, file.uri, file.name, file.mimeType || 'audio/m4a');
    } catch (e: any) {
      Alert.alert('Upload Failed', e?.response?.data?.detail || 'Please try again.');
    }
  };

  const uploadAudio = async (label: VoiceLabel, uri: string, name: string, type: string) => {
    setUploading(label);
    try {
      const formData = new FormData();
      formData.append('label', label);
      formData.append('file', { uri, name, type } as any);
      await apiClient.post('/voices/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      });
      setVoiceStatus(prev => ({ ...prev, [label.toLowerCase()]: true }));
      Alert.alert('🎉 Voice Cloned!', `${label}'s voice is ready! New stories will be narrated in your voice.`, [{ text: 'Awesome!' }]);
    } catch (e: any) {
      Alert.alert('Upload Failed', e?.response?.data?.detail || 'Please try a longer recording (30+ seconds).');
    } finally {
      setUploading(null);
    }
  };

  const formatTime = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`;

  const VoiceCard = ({ label, emoji }: { label: VoiceLabel; emoji: string }) => {
    const isReady = voiceStatus[label.toLowerCase() as keyof VoiceStatus];
    const isUploading = uploading === label;
    const isRecordingThis = recordingLabel === label;

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

        {/* Recording UI */}
        {isRecordingThis && recordingState === 'recording' && (
          <View style={styles.recordingActive}>
            <View style={styles.recordingDot} />
            <Text style={styles.recordingTime}>{formatTime(recordingSeconds)}</Text>
            <Text style={styles.recordingHint}>Speak naturally — read anything aloud</Text>
            <TouchableOpacity style={styles.stopButton} onPress={stopRecording}>
              <Text style={styles.stopButtonText}>⏹ Stop Recording</Text>
            </TouchableOpacity>
          </View>
        )}

        {isRecordingThis && recordingState === 'recorded' && (
          <View style={styles.recordingDone}>
            <Text style={styles.recordingDoneText}>✓ Recorded {formatTime(recordingSeconds)}</Text>
            <View style={styles.recordingActions}>
              <TouchableOpacity style={styles.discardButton} onPress={discardRecording}>
                <Text style={styles.discardButtonText}>Discard</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.useButton, isUploading && styles.buttonDisabled]}
                onPress={uploadRecording}
                disabled={isUploading}
              >
                {isUploading
                  ? <ActivityIndicator color={COLORS.white} size="small" />
                  : <Text style={styles.useButtonText}>Use This Recording</Text>}
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* Buttons — only show when not recording this label */}
        {(!isRecordingThis || recordingState === 'idle') && (
          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={[styles.recordButton, !canRecord && styles.buttonDimmed]}
              onPress={() => startRecording(label)}
              disabled={isUploading || (recordingState === 'recording' && !isRecordingThis)}
              activeOpacity={0.8}
            >
              <Text style={styles.recordButtonText}>🎙 Record Now</Text>
              {!canRecord && <Text style={styles.buttonSubtext}>Needs native build</Text>}
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.uploadButton, isUploading && styles.buttonDisabled]}
              onPress={() => handleUploadFile(label)}
              disabled={isUploading || recordingState === 'recording'}
              activeOpacity={0.8}
            >
              {isUploading
                ? <ActivityIndicator color={COLORS.deepIndigo} size="small" />
                : <>
                    <Text style={styles.uploadButtonText}>📁 Upload File</Text>
                    <Text style={styles.buttonSubtext}>From Voice Memos</Text>
                  </>}
            </TouchableOpacity>
          </View>
        )}
      </View>
    );
  };

  return (
    <LinearGradient colors={[COLORS.cream, '#EEF2FF']} style={styles.gradient}>
      <SafeAreaView style={styles.safe}>
        <View style={styles.header}>
          <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()} activeOpacity={0.8}>
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Parent Voices</Text>
          <Text style={styles.headerEmoji}>🎙</Text>
        </View>

        <ScrollView style={styles.scroll} contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
          <Text style={styles.subtitle}>
            Clone your voice so your children hear you narrate their bedtime stories — even when you're not there.
          </Text>

          <VoiceCard label="Mom" emoji="👩" />
          <VoiceCard label="Dad" emoji="👨" />

          <View style={styles.tipBox}>
            <Text style={styles.tipTitle}>💡 Tips for best results</Text>
            <Text style={styles.tipText}>• Record in a quiet room with no background noise</Text>
            <Text style={styles.tipText}>• Speak naturally and clearly, as if reading to your child</Text>
            <Text style={styles.tipText}>• At least 1 minute of audio works best</Text>
            <Text style={styles.tipText}>• iPhone Voice Memos → share → save to Files → upload here</Text>
          </View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: { flex: 1 },
  safe: { flex: 1 },
  scroll: { flex: 1 },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.sm,
    paddingBottom: SPACING.md,
  },
  backButton: {
    width: 48, height: 48, borderRadius: RADIUS.round,
    backgroundColor: 'rgba(45,27,105,0.1)', alignItems: 'center', justifyContent: 'center',
  },
  backButtonText: { fontSize: FONTS.sizes.lg, color: COLORS.deepIndigo, fontWeight: FONTS.weights.bold as any },
  headerTitle: { flex: 1, fontSize: FONTS.sizes.lg, fontWeight: FONTS.weights.heavy as any, color: COLORS.deepIndigo, marginLeft: SPACING.sm },
  headerEmoji: { fontSize: 28 },
  content: { paddingHorizontal: SPACING.lg, paddingBottom: SPACING.xxl },
  subtitle: { fontSize: FONTS.sizes.sm, color: COLORS.mutedText, lineHeight: 22, marginBottom: SPACING.xl },
  card: {
    backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: SPACING.lg,
    marginBottom: SPACING.md,
    shadowColor: COLORS.deepIndigo, shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08, shadowRadius: 8, elevation: 3,
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: SPACING.md },
  cardEmoji: { fontSize: 36, marginRight: SPACING.md },
  cardInfo: { flex: 1 },
  cardTitle: { fontSize: FONTS.sizes.md, fontWeight: FONTS.weights.heavy as any, color: COLORS.deepIndigo },
  cardStatus: { fontSize: FONTS.sizes.xs, marginTop: 2 },
  readyBadge: { fontSize: 24, color: '#4CAF50' },
  buttonRow: { flexDirection: 'row', gap: SPACING.sm },
  recordButton: {
    flex: 1, backgroundColor: COLORS.deepIndigo, borderRadius: RADIUS.md,
    paddingVertical: SPACING.md, alignItems: 'center', justifyContent: 'center', minHeight: 64,
  },
  recordButtonText: { color: COLORS.white, fontSize: FONTS.sizes.sm, fontWeight: FONTS.weights.bold as any },
  uploadButton: {
    flex: 1, backgroundColor: COLORS.lavender, borderRadius: RADIUS.md,
    paddingVertical: SPACING.md, alignItems: 'center', justifyContent: 'center', minHeight: 64,
  },
  uploadButtonText: { color: COLORS.deepIndigo, fontSize: FONTS.sizes.sm, fontWeight: FONTS.weights.bold as any },
  buttonSubtext: { fontSize: 10, color: 'rgba(0,0,0,0.4)', marginTop: 2 },
  buttonDimmed: { opacity: 0.5 },
  buttonDisabled: { opacity: 0.6 },
  recordingActive: {
    backgroundColor: '#FFF0F0', borderRadius: RADIUS.md, padding: SPACING.lg,
    alignItems: 'center', marginBottom: SPACING.sm,
  },
  recordingDot: {
    width: 14, height: 14, borderRadius: 7, backgroundColor: '#F44336',
    marginBottom: SPACING.sm,
  },
  recordingTime: { fontSize: FONTS.sizes.xl, fontWeight: FONTS.weights.heavy as any, color: COLORS.deepIndigo, marginBottom: 4 },
  recordingHint: { fontSize: FONTS.sizes.xs, color: COLORS.mutedText, marginBottom: SPACING.md },
  stopButton: {
    backgroundColor: '#F44336', borderRadius: RADIUS.md,
    paddingVertical: SPACING.sm, paddingHorizontal: SPACING.xl, minHeight: 48, justifyContent: 'center',
  },
  stopButtonText: { color: COLORS.white, fontWeight: FONTS.weights.bold as any },
  recordingDone: {
    backgroundColor: '#F0FFF4', borderRadius: RADIUS.md, padding: SPACING.lg,
    alignItems: 'center', marginBottom: SPACING.sm,
  },
  recordingDoneText: { fontSize: FONTS.sizes.sm, color: '#4CAF50', fontWeight: FONTS.weights.bold as any, marginBottom: SPACING.md },
  recordingActions: { flexDirection: 'row', gap: SPACING.sm, width: '100%' },
  discardButton: {
    flex: 1, borderWidth: 1, borderColor: COLORS.mutedText, borderRadius: RADIUS.md,
    paddingVertical: SPACING.sm, alignItems: 'center', minHeight: 48, justifyContent: 'center',
  },
  discardButtonText: { color: COLORS.mutedText, fontWeight: FONTS.weights.medium as any },
  useButton: {
    flex: 2, backgroundColor: COLORS.deepIndigo, borderRadius: RADIUS.md,
    paddingVertical: SPACING.sm, alignItems: 'center', minHeight: 48, justifyContent: 'center',
  },
  useButtonText: { color: COLORS.white, fontWeight: FONTS.weights.bold as any },
  tipBox: { backgroundColor: COLORS.deepIndigo + '10', borderRadius: RADIUS.md, padding: SPACING.lg, marginTop: SPACING.sm },
  tipTitle: { fontSize: FONTS.sizes.sm, fontWeight: FONTS.weights.bold as any, color: COLORS.deepIndigo, marginBottom: SPACING.sm },
  tipText: { fontSize: FONTS.sizes.xs, color: COLORS.mutedText, lineHeight: 22 },
});
