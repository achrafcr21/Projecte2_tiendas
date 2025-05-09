import React, { useState, useEffect } from 'react';
import { Plus, Search, X } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import StoreTable from '../../components/StoreTable';
import { useToast } from '../../components/Toast';
import { useAuth } from '../../context/AuthContext';
import { getStores, createStore, getUsers } from '../../services/api';

export default function Stores() {
  const location = useLocation();
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(location.state?.showCreateModal || false);
  const [newStore, setNewStore] = useState({
    nombre: '',
    descripcion: '',
    propietario: ''
  });
  const [users, setUsers] = useState([]);
  const { addToast } = useToast();
  const { user } = useAuth();

  useEffect(() => {
    loadStores();
    if (user?.rol === 'admin') {
      loadUsers();
    }
  }, [user?.rol]);

  const loadStores = async () => {
    try {
      const data = await getStores();
      setStores(data);
    } catch (error) {
      addToast(error.message || 'Error al cargar las tiendas', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data.filter(u => u.rol !== 'admin')); // Solo mostrar usuarios no admin
    } catch (error) {
      addToast('Error al cargar usuarios', 'error');
    }
  };

  const handleCreateStore = async (e) => {
    e.preventDefault();
    try {
      await createStore(newStore);
      addToast('Tienda creada correctamente', 'success');
      setShowCreateModal(false);
      setNewStore({ nombre: '', descripcion: '', propietario: '' });
      loadStores();
    } catch (error) {
      addToast(error.message || 'Error al crear la tienda', 'error');
    }
  };

  const filteredStores = stores.filter(store => 
    store.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    store.descripcion.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
            {user?.rol === 'admin' ? 'Gestión de Tiendas' : 'Mis Tiendas'}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            {user?.rol === 'admin' 
              ? 'Administra todas las tiendas registradas en la plataforma'
              : 'Gestiona tus tiendas digitalizadas'
            }
          </p>
        </div>
        {user?.rol === 'admin' && (
          <div className="mt-4 sm:mt-0">
            <button
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <Plus className="-ml-1 mr-2 h-5 w-5" />
              Nueva Tienda
            </button>
          </div>
        )}
      </div>

      {/* Barra de búsqueda */}
      <div className="max-w-lg w-full">
        <div className="mt-1 relative rounded-md shadow-sm">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md"
            placeholder="Buscar tiendas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {filteredStores.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {searchTerm ? 'No se encontraron tiendas' : 'No hay tiendas'}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm 
              ? 'Intenta con otros términos de búsqueda'
              : user?.rol === 'admin'
                ? 'Comienza creando una nueva tienda'
                : 'No tienes tiendas asignadas aún'
            }
          </p>
          {user?.rol === 'admin' && !searchTerm && (
            <div className="mt-6">
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              >
                <Plus className="-ml-1 mr-2 h-5 w-5" />
                Crear Primera Tienda
              </button>
            </div>
          )}
        </div>
      ) : (
        <StoreTable
          stores={filteredStores}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
          isAdmin={user?.rol === 'admin'}
        />
      )}

      {/* Modal de crear tienda */}
      {showCreateModal && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

            <div className="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <div className="absolute top-0 right-0 pt-4 pr-4">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  <span className="sr-only">Cerrar</span>
                  <X className="h-6 w-6" />
                </button>
              </div>

              <form onSubmit={handleCreateStore}>
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Nueva Tienda
                  </h3>
                  <div className="mt-2">
                    <input
                      type="text"
                      required
                      className="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="Nombre de la tienda"
                      value={newStore.nombre}
                      onChange={(e) => setNewStore({ ...newStore, nombre: e.target.value })}
                    />
                  </div>
                  <div className="mt-2">
                    <textarea
                      required
                      rows={3}
                      className="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="Descripción"
                      value={newStore.descripcion}
                      onChange={(e) => setNewStore({ ...newStore, descripcion: e.target.value })}
                    />
                  </div>
                  <div className="mt-2">
                    <select
                      required
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
                      value={newStore.propietario}
                      onChange={(e) => setNewStore({ ...newStore, propietario: e.target.value })}
                    >
                      <option value="">Seleccionar propietario</option>
                      {users.map((user) => (
                        <option key={user.id} value={user.id}>
                          {user.username} ({user.email})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:col-start-2 sm:text-sm"
                  >
                    Crear
                  </button>
                  <button
                    type="button"
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:col-start-1 sm:text-sm"
                    onClick={() => setShowCreateModal(false)}
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
