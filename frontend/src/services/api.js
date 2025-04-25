import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
});

// Interceptor para añadir el token a las peticiones
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Autenticación
export const login = async (credentials) => {
  try {
    const response = await api.post('/login/', credentials);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error en el inicio de sesión');
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/registro/', userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error en el registro');
  }
};

// Tiendas
export const createStore = async (storeData) => {
  try {
    const response = await api.post('/tiendas/', storeData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al crear la tienda');
  }
};

export const getStoreDetails = async (storeId) => {
  try {
    const response = await api.get(`/tiendas/${storeId}/`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener los detalles de la tienda');
  }
};

// Productos
export const getProducts = async () => {
  try {
    const response = await api.get('/productos/');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener los productos');
  }
};

export const createProduct = async (productData) => {
  try {
    const response = await api.post('/productos/', productData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al crear el producto');
  }
};

// Pedidos
export const getOrders = async () => {
  try {
    const response = await api.get('/pedidos/');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener los pedidos');
  }
};

export const createOrder = async (orderData) => {
  try {
    const response = await api.post('/pedidos/', orderData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al crear el pedido');
  }
};

export default api;
