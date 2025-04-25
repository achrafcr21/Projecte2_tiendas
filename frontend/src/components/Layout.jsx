import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

const Layout = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const isAuthenticated = localStorage.getItem('token');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              {/* Logo */}
              <Link to="/" className="flex-shrink-0 flex items-center">
                <span className="text-xl font-bold text-primary">DigiTiendas</span>
              </Link>
            </div>

            {/* Desktop menu */}
            <div className="hidden md:flex md:items-center md:space-x-4">
              <Link to="/" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Inicio
              </Link>
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                    Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      localStorage.removeItem('token');
                      window.location.href = '/';
                    }}
                    className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Cerrar sesión
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                    Iniciar sesión
                  </Link>
                  <Link to="/registro" className="bg-primary text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-dark">
                    Registrarse
                  </Link>
                </>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary focus:outline-none"
              >
                {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <Link to="/" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary">
                Inicio
              </Link>
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary">
                    Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      localStorage.removeItem('token');
                      window.location.href = '/';
                    }}
                    className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary"
                  >
                    Cerrar sesión
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary">
                    Iniciar sesión
                  </Link>
                  <Link to="/registro" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary">
                    Registrarse
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </nav>

      {/* Main content */}
      <main>{children}</main>
    </div>
  );
};

export default Layout;
