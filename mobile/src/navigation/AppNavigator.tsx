import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import ProfileSelectScreen from '../screens/ProfileSelectScreen';
import StoryModeSelectScreen from '../screens/StoryModeSelectScreen';
import ThemePickerScreen from '../screens/ThemePickerScreen';
import VoicePickerScreen from '../screens/VoicePickerScreen';
import StoryLibraryScreen from '../screens/StoryLibraryScreen';
import StoryPlayerScreen from '../screens/StoryPlayerScreen';
import SleepModeScreen from '../screens/SleepModeScreen';
import ParentPasscodeScreen from '../screens/ParentPasscodeScreen';
import ParentDashboardScreen from '../screens/ParentDashboardScreen';
import AddProfileScreen from '../screens/AddProfileScreen';
import { useAuthStore } from '../store/authStore';
import { COLORS } from '../constants/theme';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const { token, loadStoredToken } = useAuthStore();
  const [isReady, setIsReady] = useState(false);
  const [hasToken, setHasToken] = useState(false);

  useEffect(() => {
    const init = async () => {
      const found = await loadStoredToken();
      setHasToken(found);
      setIsReady(true);
    };
    init();
  }, []);

  if (!isReady) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={COLORS.deepIndigo} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{ headerShown: false, animation: 'slide_from_right' }}
        initialRouteName={hasToken ? 'ProfileSelect' : 'Login'}
      >
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="ProfileSelect" component={ProfileSelectScreen} />
        <Stack.Screen name="StoryModeSelect" component={StoryModeSelectScreen} />
        <Stack.Screen name="ThemePicker" component={ThemePickerScreen} />
        <Stack.Screen name="VoicePicker" component={VoicePickerScreen} />
        <Stack.Screen name="StoryLibrary" component={StoryLibraryScreen} />
        <Stack.Screen
          name="StoryPlayer"
          component={StoryPlayerScreen}
          options={{ animation: 'fade' }}
        />
        <Stack.Screen
          name="SleepMode"
          component={SleepModeScreen}
          options={{ animation: 'fade', gestureEnabled: false }}
        />
        <Stack.Screen name="ParentPasscode" component={ParentPasscodeScreen} />
        <Stack.Screen name="ParentDashboard" component={ParentDashboardScreen} />
        <Stack.Screen name="AddProfile" component={AddProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF8E7',
  },
});
