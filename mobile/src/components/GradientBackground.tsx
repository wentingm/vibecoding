import React from 'react';
import { StyleSheet, ViewStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface GradientBackgroundProps {
  colors: string[];
  children?: React.ReactNode;
  style?: ViewStyle;
  start?: { x: number; y: number };
  end?: { x: number; y: number };
}

export default function GradientBackground({
  colors,
  children,
  style,
  start = { x: 0, y: 0 },
  end = { x: 0, y: 1 },
}: GradientBackgroundProps) {
  return (
    <LinearGradient
      colors={colors as [string, string, ...string[]]}
      style={[styles.container, style]}
      start={start}
      end={end}
    >
      {children}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
