import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_URL = 'http://10.100.1.95:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Attach JWT token to every request
apiClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
