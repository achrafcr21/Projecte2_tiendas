from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Usuario
from .serializers import UsuarioSerializer
from django.db import transaction

@api_view(['POST'])
def registro_usuario(request):
    """
    Registra un nuevo usuario en el sistema.
    
    Requiere:
    - email: correo electrónico único
    - username: nombre de usuario único
    - password: contraseña
    - password2: confirmación de contraseña
    - rol: rol del usuario (opcional, por defecto 'cliente')
    """
    try:
        with transaction.atomic():
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.save()
                # Creamos un nuevo serializer solo para la respuesta
                response_serializer = UsuarioSerializer(usuario)
                return Response({
                    'mensaje': 'Usuario registrado correctamente',
                    'usuario': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'error': 'Error en los datos proporcionados',
                'detalles': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Error al registrar usuario',
            'detalles': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
