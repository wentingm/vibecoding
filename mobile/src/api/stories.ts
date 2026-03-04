import { apiClient } from './client';

export const getCuratedStories = (themes?: string[]) => {
  const params = themes?.length ? { themes: themes.join(',') } : {};
  return apiClient.get('/stories', { params });
};

export const getStory = (id: string) => apiClient.get(`/stories/${id}`);

export const generateStory = (data: {
  child_name: string;
  themes: string[];
  child_profile_id: string;
  voice: string;
}) => apiClient.post('/stories/generate', data);

export const logSession = (data: any) => apiClient.post('/stories/sessions', data);
export const completeSession = (sessionId: string, data: any) =>
  apiClient.put(`/stories/sessions/${sessionId}`, data);
