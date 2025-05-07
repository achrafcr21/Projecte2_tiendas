import React from 'react';
import { Check } from 'lucide-react';

export default function ServiceCard({ service, onSelect, isSelected }) {
  return (
    <div
      className={`relative p-6 bg-white rounded-lg border-2 transition-all ${
        isSelected
          ? 'border-primary shadow-lg scale-105'
          : 'border-gray-200 hover:border-primary/50'
      }`}
    >
      {isSelected && (
        <div className="absolute top-4 right-4">
          <Check className="h-6 w-6 text-primary" />
        </div>
      )}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">{service.nombre}</h3>
        <p className="text-sm text-gray-500">{service.descripcion}</p>
        <div className="flex justify-between items-center">
          <span className="text-2xl font-bold text-gray-900">
            {service.precio.toLocaleString('es-ES', {
              style: 'currency',
              currency: 'EUR'
            })}
          </span>
          <button
            onClick={() => onSelect(service)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              isSelected
                ? 'bg-primary text-white hover:bg-primary-dark'
                : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
            }`}
          >
            {isSelected ? 'Seleccionado' : 'Seleccionar'}
          </button>
        </div>
      </div>
    </div>
  );
}
