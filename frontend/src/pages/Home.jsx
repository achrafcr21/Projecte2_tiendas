import { useNavigate } from 'react-router-dom';
import { Store, Globe, ShoppingBag } from 'lucide-react';

const ServiceCard = ({ icon: Icon, title, description }) => (
  <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
    <div className="flex items-center justify-center w-12 h-12 bg-primary rounded-full mb-4">
      <Icon className="text-white" size={24} />
    </div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const Home = () => {
  const navigate = useNavigate();

  const services = [
    {
      icon: Store,
      title: "Tienda Online",
      description: "Crea tu tienda online profesional con todas las funcionalidades necesarias para vender en internet."
    },
    {
      icon: Globe,
      title: "Presencia Digital",
      description: "Mejora tu visibilidad en internet con una web moderna y optimizada para buscadores."
    },
    {
      icon: ShoppingBag,
      title: "Gestión de Pedidos",
      description: "Sistema completo para gestionar tus pedidos, inventario y clientes de forma eficiente."
    }
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="bg-primary text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Digitaliza tu Negocio
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-2xl mx-auto">
              Transforma tu tienda física en un negocio digital. Alcanza más clientes y aumenta tus ventas.
            </p>
            <button
              onClick={() => navigate('/solicitud')}
              className="bg-white text-primary px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors"
            >
              Solicita tu Digitalización
            </button>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">¿Qué Ofrecemos?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <ServiceCard key={index} {...service} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">¿Listo para dar el salto digital?</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Únete a los cientos de negocios que ya han confiado en nosotros para su transformación digital.
          </p>
          <button
            onClick={() => navigate('/servicios')}
            className="bg-primary text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-primary-dark transition-colors"
          >
            Ver Nuestros Servicios
          </button>
        </div>
      </section>
    </div>
  );
};

export default Home;
