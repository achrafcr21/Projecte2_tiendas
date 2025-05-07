import React, { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import StoreTable from '../../components/StoreTable';
import { useToast } from '../../components/Toast';
import { getStores } from '../../services/api';

export default function Stores() {
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => {
    loadStores();
  }, []);

  const loadStores = async () => {
    try {
      const data = await getStores();
      setStores(data);
    } catch (error) {
      addToast('Error al cargar las tiendas', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleView = (store) => {
    // TODO: Implementar vista detallada
    console.log('Ver tienda:', store);
  };

  const handleEdit = (store) => {
    // TODO: Implementar edición
    console.log('Editar tienda:', store);
  };

  const handleDelete = (store) => {
    // TODO: Implementar eliminación
    console.log('Eliminar tienda:', store);
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">
            Tiendas
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Gestiona las tiendas registradas en la plataforma
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            type="button"
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            <Plus className="-ml-1 mr-2 h-5 w-5" />
            Nueva Tienda
          </button>
        </div>
      </div>

      {stores.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay tiendas</h3>
          <p className="mt-1 text-sm text-gray-500">
            Comienza creando una nueva tienda.
          </p>
        </div>
      ) : (
        <StoreTable
          stores={stores}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}
