import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = () => api.get('/health');

export const getMajors = () => api.get('/majors');

export const getMajor = (majorId) => api.get(`/major/${majorId}`);

export const sendChatMessage = (message, context = {}) =>
  api.post('/chat', { message, context });

export const generateSchedule = (majors, semester = 'Fall') =>
  api.post('/schedule', { majors, semester });

export const compareMajors = (majors) =>
  api.post('/compare', { majors });

export default api;
