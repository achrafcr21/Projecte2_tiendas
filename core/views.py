from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer, TiendaSerializer, ProductoSerializer, PedidoSerializer, SolicitudSerializer, ServicioSerializer, TiendaServicioSerializer
from .models import Usuario, Tienda, Solicitud, Servicio, TiendaServicio
from .permissions import IsAdminUser, IsAdmin
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

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
    """
    Vista per llistar totes les tiendas i crear-ne de noves.
    GET: Qualsevol usuari autenticat pot veure les tiendas
    POST: Només els usuaris admin poden crear tiendas
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        # Guardem la tienda amb l'usuari admin com a propietari
        serializer.save(propietario=self.request.user)

class TiendaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista per gestionar una tienda específica.
    GET: Qualsevol usuari autenticat pot veure els detalls
    PUT/DELETE: Només el propietari (admin) pot modificar o eliminar
    """
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class SolicitudCreateView(generics.CreateAPIView):
    """
    Vista per crear noves sol·licituds de digitalització.
    No requereix autenticació ja que és per clients potencials.
    """
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "missatge": "Sol·licitud enviada correctament. Et contactarem aviat.",
                "id": serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudListView(generics.ListAPIView):
    """
    Vista per llistar sol·licituds.
    Només accessible per admins.
    """
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class SolicitudDetailView(generics.RetrieveUpdateAPIView):
    """
    Vista per veure i actualitzar una sol·licitud específica.
    Només accessible per admins.
    """
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Validar el estado si se está actualizando
        if 'estado' in request.data and request.data['estado'] not in dict(Solicitud.ESTADO_CHOICES):
            return Response({
                'error': f'Estado inválido. Opciones válidas: {", ".join(dict(Solicitud.ESTADO_CHOICES).keys())}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "mensaje": "Solicitud actualizada correctamente",
                "solicitud": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServicioListView(generics.ListCreateAPIView):
    """
    Vista per llistar i crear serveis.
    GET: Tothom pot veure els serveis actius
    POST: Només els admins poden crear serveis
    """
    serializer_class = ServicioSerializer
    
    def get_queryset(self):
        # Si no és admin, només mostrem serveis actius
        if not self.request.user or self.request.user.rol != 'admin':
            return Servicio.objects.filter(activo=True)
        return Servicio.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return []

class TiendaServicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet pels serveis d'una botiga.
    Permet gestionar els serveis assignats a una botiga específica.
    """
    serializer_class = TiendaServicioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        tienda_id = self.kwargs['tienda_id']
        tienda = get_object_or_404(Tienda, id=tienda_id)
        
        # Verificar permisos
        if self.request.user.rol != 'admin' and tienda.propietario != self.request.user:
            raise PermissionDenied(
                "No tens permís per veure els serveis d'aquesta botiga"
            )
            
        return TiendaServicio.objects.filter(tienda=tienda)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        tienda_id = self.kwargs['tienda_id']
        context['tienda'] = get_object_or_404(Tienda, id=tienda_id)
        return context
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
