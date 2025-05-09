import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardLayout from './components/DashboardLayout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Stores from './pages/Dashboard/Stores';
import Services from './pages/Dashboard/Services';
import Support from './pages/Dashboard/Support';
import Settings from './pages/Dashboard/Settings';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './components/Toast';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <Router>
          <Routes>
            {/* Rutas públicas */}
            <Route path="/" element={<Layout><Home /></Layout>} />
            <Route path="/login" element={<Login />} />
            <Route path="/registro" element={<Register />} />

            {/* Rutas protegidas del dashboard */}
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <DashboardLayout>
                    <Dashboard />
                  </DashboardLayout>
                </PrivateRoute>
              }
            />

            {/* Rutas protegidas adicionales */}
            <Route
              path="/dashboard/tiendas"
              element={
                <PrivateRoute>
                  <DashboardLayout>
                    <Stores />
                  </DashboardLayout>
                </PrivateRoute>
              }
            />

            {/* Nueva ruta para servicios */}
            <Route
              path="/dashboard/servicios"
              element={
                <PrivateRoute>
                  <DashboardLayout>
                    <Services />
                  </DashboardLayout>
                </PrivateRoute>
              }
            />

            {/* Ruta para soporte */}
            <Route
              path="/dashboard/soporte"
              element={
                <PrivateRoute>
                  <DashboardLayout>
                    <Support />
                  </DashboardLayout>
                </PrivateRoute>
              }
            />

            {/* Ruta para configuración */}
            <Route
              path="/dashboard/configuracion"
              element={
                <PrivateRoute>
                  <DashboardLayout>
                    <Settings />
                  </DashboardLayout>
                </PrivateRoute>
              }
            />

            {/* Ruta por defecto - redirige a home */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
