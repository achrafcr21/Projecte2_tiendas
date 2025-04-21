from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import views_dam  # Importar vistas de DAM

app_name = 'core'

# Crear router per les vistes basades en ViewSet
router = DefaultRouter()
router.register(r'tiendas/(?P<tienda_id>\d+)/servicios', views.TiendaServicioViewSet, basename='tienda-servicios')
router.register(r'pagos', views.PagoViewSet, basename='pagos')
router.register(r'soporte', views.SoporteViewSet, basename='soporte')

urlpatterns = [
    # Autenticación
    path('api/registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('api/login/', views.login_view, name='login'),
    
    # Tiendas (solo lectura para clientes)
    path('api/tiendas/', views.TiendaListCreateView.as_view(), name='tienda-list'),
    path('api/tiendas/<int:pk>/', views.TiendaDetailView.as_view(), name='tienda-detail'),
    
    # Solicitudes de digitalización
    path('api/solicitudes/', views.SolicitudListView.as_view(), name='solicitud-list'),
    path('api/solicitudes/crear/', views.SolicitudCreateView.as_view(), name='solicitud-create'),
    path('api/solicitudes/<int:pk>/', views.SolicitudDetailView.as_view(), name='solicitud-detail'),
    
    # Noves URLs de serveis
    path('api/servicios/', views.ServicioListView.as_view(), name='servicio-list'),
    
    # Incloure les URLs del router
    path('api/', include(router.urls)),
    
    # URLs de la APP MÓVIL (DAM)
    path('api/app/', include('core.urls_dam')),
]