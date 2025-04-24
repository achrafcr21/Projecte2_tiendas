import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token a las peticiones
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Auth services
export const login = async (credentials) => {
  const response = await api.post('/login/', credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/registro/', userData);
  return response.data;
};

// Services
export const getServices = async () => {
  const response = await api.get('/servicios/');
  return response.data;
};

// Requests
export const createRequest = async (requestData) => {
  const response = await api.post('/solicitudes/crear/', requestData);
  return response.data;
};

export default api;
