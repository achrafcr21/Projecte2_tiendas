from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer, TiendaSerializer, ProductoSerializer, PedidoSerializer
from .models import Usuario, Tienda

# Create your views here.

class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"mensaje": "Usuario registrado correctamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Por favor proporcione email y contraseña'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=email, password=password)
    if user:
        return Response({'mensaje': 'Login exitoso'}, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Credenciales inválidas'},
        status=status.HTTP_401_UNAUTHORIZED
    )

class TiendaListCreateView(generics.ListCreateAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)
