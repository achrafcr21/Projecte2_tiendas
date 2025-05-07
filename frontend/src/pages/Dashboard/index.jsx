import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

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
            {user?.tiendas?.length || 0}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Servicios Activos</h3>
          <p className="mt-2 text-3xl font-bold text-primary">
            {user?.servicios_activos || 0}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Tickets de Soporte</h3>
          <p className="mt-2 text-3xl font-bold text-primary">
            {user?.tickets_pendientes || 0}
          </p>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="mt-8">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Acciones Rápidas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <button
            onClick={() => navigate('/dashboard/tiendas')}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark"
          >
            Nueva Tienda
          </button>
          <button
            onClick={() => navigate('/dashboard/soporte')}
            className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            Crear Ticket
          </button>
        </div>
      </div>
    </div>
  );
}
