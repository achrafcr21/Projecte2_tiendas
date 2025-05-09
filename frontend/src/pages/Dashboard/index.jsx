import React, { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { getUserStats } from '../../services/api';
import { useToast } from '../../components/Toast';

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [stats, setStats] = useState({
    tiendas: 0,
    servicios_activos: 0,
    tickets_pendientes: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await getUserStats();
        setStats(data);
      } catch (error) {
        console.error('Error al cargar estadísticas:', error);
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []); // Quitamos addToast de las dependencias

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">
          Bienvenido, {user?.username}
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Panel de control de tu negocio digital
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Estadísticas y resumen */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Tus Tiendas</h3>
          <p className="mt-2 text-3xl font-bold text-primary">
            {loading ? '...' : stats.tiendas}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Servicios Activos</h3>
          <p className="mt-2 text-3xl font-bold text-primary">
            {loading ? '...' : stats.servicios_activos}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Tickets de Soporte</h3>
          <p className="mt-2 text-3xl font-bold text-primary">
            {loading ? '...' : stats.tickets_pendientes}
          </p>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="mt-8">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Acciones Rápidas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <button
            onClick={() => navigate('/dashboard/tiendas', { state: { showCreateModal: user?.rol === 'admin' } })}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark"
          >
            <Plus className="-ml-1 mr-2 h-5 w-5" />
            {user?.rol === 'admin' ? 'Crear Nueva Tienda' : 'Ver Mis Tiendas'}
          </button>
          <button
            onClick={() => navigate('/dashboard/servicios')}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark"
          >
            Servicios Disponibles
          </button>
          <button
            onClick={() => navigate('/dashboard/soporte')}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark"
          >
            Soporte Técnico
          </button>
        </div>
      </div>
    </div>
  );
}
