import { useNavigate } from 'react-router-dom';
import { Menu, X, LogOut } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-primary text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold">Digitalización Tiendas</h1>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="/" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark">Inicio</a>
                <a href="/servicios" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark">Servicios</a>
                {isAuthenticated ? (
                  <>
                    <a href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark">Dashboard</a>
                    <button onClick={handleLogout} className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark flex items-center">
                      <LogOut className="w-4 h-4 mr-2" />
                      Cerrar Sesión
                    </button>
                  </>
                ) : (
                  <a href="/login" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark">Iniciar Sesión</a>
                )}
              </div>
            </div>
          </div>
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md hover:bg-primary-dark focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <a href="/" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark">Inicio</a>
            <a href="/servicios" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark">Servicios</a>
            {isAuthenticated ? (
              <>
                <a href="/dashboard" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark">Dashboard</a>
                <button onClick={handleLogout} className="w-full text-left px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark flex items-center">
                  <LogOut className="w-4 h-4 mr-2" />
                  Cerrar Sesión
                </button>
              </>
            ) : (
              <a href="/login" className="block px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark">Iniciar Sesión</a>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Contacto</h3>
            <p>Email: info@digitalizacion.com</p>
            <p>Tel: +34 123 456 789</p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Enlaces</h3>
            <ul className="space-y-2">
              <li><a href="/servicios" className="hover:text-gray-300">Servicios</a></li>
              <li><a href="/solicitud" className="hover:text-gray-300">Solicitar Digitalización</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><a href="/privacidad" className="hover:text-gray-300">Política de Privacidad</a></li>
              <li><a href="/terminos" className="hover:text-gray-300">Términos y Condiciones</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 text-center">
          <p>&copy; {new Date().getFullYear()} Digitalización Tiendas. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
