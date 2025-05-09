import React, { useState } from 'react';
import { Menu, Bell, User, Settings, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import { useNavigate } from 'react-router-dom';

export default function DashboardHeader({ toggleSidebar }) {
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    addToast('Sesión cerrada correctamente', 'success');
    navigate('/login');
  };

  const handleSettings = () => {
    setIsProfileMenuOpen(false);
    navigate('/dashboard/configuracion');
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <button
              onClick={toggleSidebar}
              className="md:hidden px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>

          <div className="flex items-center">
            {/* Notificaciones */}
            <button className="p-2 text-gray-400 hover:text-gray-500">
              <Bell className="h-6 w-6" />
            </button>

            {/* Perfil */}
            <div className="ml-3 relative">
              <div>
                <button 
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                  className="flex items-center max-w-xs rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  <span className="sr-only">Abrir menú de usuario</span>
                  <div className="flex items-center">
                    <User className="h-8 w-8 rounded-full p-1 border-2 border-gray-300" />
                    <span className="ml-2 text-sm text-gray-700 hidden md:block">
                      {user?.username}
                    </span>
                  </div>
                </button>
              </div>

              {/* Menú desplegable */}
              {isProfileMenuOpen && (
                <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100">
                  <div className="py-1">
                    <button
                      onClick={handleSettings}
                      className="group flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <Settings className="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" />
                      Configuración
                    </button>
                  </div>
                  <div className="py-1">
                    <button
                      onClick={handleLogout}
                      className="group flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <LogOut className="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" />
                      Cerrar sesión
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
