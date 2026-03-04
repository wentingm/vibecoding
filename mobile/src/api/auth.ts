import { apiClient } from './client';

export const register = (email: string, password: string, family_name: string) =>
  apiClient.post('/auth/register', { email, password, family_name });

export const login = (email: string, password: string) =>
  apiClient.post('/auth/login', { email, password });

export const getMe = () => apiClient.get('/auth/me');
