import React, { useMemo } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const STARS = ['⭐', '✨', '⭐', '✨', '⭐', '✨', '⭐', '✨', '⭐', '✨', '⭐', '✨', '⭐'];

interface StarBackgroundProps {
  count?: number;
}

export default function StarBackground({ count = 12 }: StarBackgroundProps) {
  const stars = useMemo(() => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      emoji: STARS[i % STARS.length],
      top: Math.random() * (height * 0.9),
      left: Math.random() * (width * 0.95),
      size: 10 + Math.random() * 14,
      opacity: 0.3 + Math.random() * 0.5,
    }));
  }, [count]);

  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none">
      {stars.map((star) => (
        <Text
          key={star.id}
          style={[
            styles.star,
            {
              top: star.top,
              left: star.left,
              fontSize: star.size,
              opacity: star.opacity,
            },
          ]}
        >
          {star.emoji}
        </Text>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  star: {
    position: 'absolute',
  },
});
