import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un token y datos de usuario almacenados
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('userData');
    if (token && userData) {
      setUser({ ...JSON.parse(userData), token });
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const data = await apiLogin(credentials);
      if (data.token) {
        localStorage.setItem('token', data.token);
        // Guardar datos completos del usuario
        const userData = {
          id: data.id,
          username: data.username,
          email: data.email,
          rol: data.rol
        };
        localStorage.setItem('userData', JSON.stringify(userData));
        setUser({ ...userData, token: data.token });
      }
      return data;
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const data = await apiRegister(userData);
      return data;
    } catch (error) {
      console.error('Error en el registro:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userData');
    setUser(null);
  };

  if (loading) {
    return null; // o un componente de carga
  }

  const value = {
    user,
    login,
    logout,
    register,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export default AuthContext;
