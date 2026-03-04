import { apiClient } from './client';

export const getProfiles = () => apiClient.get('/profiles');
export const createProfile = (data: any) => apiClient.post('/profiles', data);
export const updateProfile = (id: string, data: any) => apiClient.put(`/profiles/${id}`, data);
export const getVoiceProfiles = (profileId: string) => apiClient.get(`/profiles/${profileId}/voice`);
