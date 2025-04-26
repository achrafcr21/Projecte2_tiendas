from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, views_dam

app_name = 'core'

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
    
    # Nuevos endpoints para usuarios
    path('api/usuarios/', views.UsuarioListView.as_view(), name='usuario-list'),
    path('api/usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),
    
    # Endpoints de carrito (APP MÓVIL - DAM)
    path('api/carrito/<int:usuario_id>/', views_dam.ver_carrito, name='ver_carrito'),
    path('api/carrito/actualizar/<int:usuario_id>/<int:producto_id>/', views_dam.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('api/carrito/vaciar/<int:usuario_id>/', views_dam.vaciar_carrito, name='vaciar_carrito'),
    path('api/carrito/crear-pedido/<int:usuario_id>/', views_dam.crear_pedido_desde_carrito, name='crear_pedido_desde_carrito'),
    path('api/carrito/añadir/<int:usuario_id>/<int:tienda_id>/', views_dam.añadir_al_carrito, name='añadir_al_carrito'),
    path('api/carrito/borrar/<int:usuario_id>/<int:producto_id>/', views_dam.borrar_del_carrito, name='borrar_del_carrito'),
    
    # Endpoints de pedidos (APP MÓVIL - DAM)
    path('api/pedidos/', views_dam.listar_pedidos, name='listar_pedidos'),
    path('api/pedidos/<int:pedido_id>/', views_dam.ver_pedido, name='ver_pedido'),
    
    # Incloure les URLs del router
    path('api/', include(router.urls)),
    
    # URLs de la APP MÓVIL (DAM)
    path('api/app/', include('core.urls_dam')),
]