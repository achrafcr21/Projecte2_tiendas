from django.urls import path
from . import views_dam

# URLs específicas para la APP MÓVIL (DAM)
urlpatterns = [
    # Endpoints de productos
    path('productos/', views_dam.listar_productos, name='dam-productos-list'),
    path('productos/crear/', views_dam.crear_producto, name='dam-producto-crear'),
    path('productos/<int:producto_id>/', views_dam.producto_detalle, name='dam-producto-detalle'),
    path('productos-vendidos/', views_dam.productos_vendidos, name='dam-productos-vendidos'),
    path('producto-mas-vendido/', views_dam.producto_mas_vendido, name='dam-producto-mas-vendido'),
    
    # Endpoints de pedidos
    path('pedidos/', views_dam.todos_los_pedidos, name='dam-pedidos-todos'),
    path('pedidos/ultimos/', views_dam.ultimos_cinco_pedidos, name='dam-pedidos-ultimos'),
    path('pedidos/<int:pedido_id>/', views_dam.detalle_pedido, name='dam-pedido-detalle'),
    path('usuario/<int:usuario_id>/pedidos/', views_dam.pedidos_usuario, name='dam-pedidos-usuario'),
    path('pedidos/estado/<str:estado>/', views_dam.pedidos_por_estado, name='dam-pedidos-estado'),
    path('pedidos/<int:pedido_id>/estado/<str:estado>/', views_dam.actualizar_estado_pedido, name='dam-actualizar-estado-pedido'),
    
    # Endpoints de carrito
    path('usuario/<int:usuario_id>/carrito/', views_dam.añadir_al_carrito, name='dam-añadir-carrito'),
    path('usuario/<int:usuario_id>/carrito/<int:producto_id>/', views_dam.borrar_del_carrito, name='dam-borrar-carrito'),
]
