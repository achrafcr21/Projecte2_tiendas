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
export const getStores = async () => {
  try {
    const response = await api.get('/tiendas/');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener las tiendas');
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

export const createStore = async (storeData) => {
  try {
    const response = await api.post('/tiendas/', storeData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al crear la tienda');
  }
};

export const updateStore = async (storeId, storeData) => {
  try {
    const response = await api.put(`/tiendas/${storeId}/`, storeData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al actualizar la tienda');
  }
};

export const deleteStore = async (storeId) => {
  try {
    await api.delete(`/tiendas/${storeId}/`);
    return true;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al eliminar la tienda');
  }
};

// Servicios
export const getServices = async () => {
  try {
    const response = await api.get('/servicios/');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener los servicios');
  }
};

export const getStoreServices = async (storeId) => {
  try {
    const response = await api.get(`/tiendas/${storeId}/servicios/`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al obtener los servicios de la tienda');
  }
};

export const contractService = async (storeId, serviceId, customPrice = null) => {
  try {
    const data = {
      servicio_id: serviceId,
      precio_final: customPrice
    };
    const response = await api.post(`/tiendas/${storeId}/servicios/`, data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al contratar el servicio');
  }
};

export const updateServiceStatus = async (storeId, serviceId, status) => {
  try {
    const response = await api.patch(`/tiendas/${storeId}/servicios/${serviceId}/`, {
      estado: status
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error al actualizar el estado del servicio');
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
