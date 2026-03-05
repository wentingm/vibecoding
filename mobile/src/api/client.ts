import axios from 'axios';
import * as SecureStore from 'expo-secure-store';
import Constants from 'expo-constants';

// Simulator uses local IP directly; real device goes through tunnel
const LOCAL_API  = 'http://10.100.1.95:8000/api/v1';
const TUNNEL_API = 'https://shy-jokes-rush.loca.lt/api/v1';

const API_URL = Constants.isDevice ? TUNNEL_API : LOCAL_API;
export const API_BASE_URL = API_URL;

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: Constants.isDevice ? { 'bypass-tunnel-reminder': 'true' } : {},
});

// Attach JWT token to every request
apiClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
