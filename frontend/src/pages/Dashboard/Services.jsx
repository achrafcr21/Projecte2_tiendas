import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import ServiceCard from '../../components/ServiceCard';
import { useToast } from '../../components/Toast';
import { getServices, contractService } from '../../services/api';

export default function Services() {
  const [services, setServices] = useState([]);
  const [selectedServices, setSelectedServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const { storeId } = useParams();
  const { addToast } = useToast();

  const loadServices = useCallback(async () => {
    try {
      const data = await getServices();
      setServices(data);
    } catch (error) {
      addToast('Error al cargar los servicios', 'error');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    loadServices();
  }, [loadServices]);

  const handleServiceSelect = (service) => {
    setSelectedServices((prev) => {
      const isSelected = prev.some((s) => s.id === service.id);
      if (isSelected) {
        return prev.filter((s) => s.id !== service.id);
      }
      return [...prev, service];
    });
  };

  const handleContractServices = async () => {
    if (!selectedServices.length) {
      addToast('Por favor, selecciona al menos un servicio', 'warning');
      return;
    }

    try {
      for (const service of selectedServices) {
        await contractService(storeId, service.id);
      }
      addToast('Servicios contratados con éxito', 'success');
      setSelectedServices([]);
    } catch (error) {
      addToast(
        error.message || 'Error al contratar los servicios',
        'error'
      );
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-48 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">
            Servicios Disponibles
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Selecciona los servicios que deseas contratar para tu tienda
          </p>
        </div>
        {selectedServices.length > 0 && (
          <button
            onClick={handleContractServices}
            className="mt-4 sm:mt-0 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Contratar Servicios Seleccionados
          </button>
        )}
      </div>

      {services.length === 0 ? (
        <div className="text-center py-12">
          <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            No hay servicios disponibles
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            No hay servicios disponibles en este momento.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service) => (
            <ServiceCard
              key={service.id}
              service={service}
              onSelect={handleServiceSelect}
              isSelected={selectedServices.some((s) => s.id === service.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
