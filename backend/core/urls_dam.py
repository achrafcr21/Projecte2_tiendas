from django.urls import path
from . import views_dam

# URLs específicas para la APP MÓVIL (DAM)
urlpatterns = [
    # Endpoints de productos
    path('productos-vendidos/', views_dam.productos_vendidos, name='productos-vendidos'),
    path('producto-mas-vendido/', views_dam.producto_mas_vendido, name='producto-mas-vendido'),
    
    # Endpoints de pedidos
    path('usuario/<int:usuario_id>/pedidos/', views_dam.pedidos_usuario, name='pedidos-usuario'),
    path('pedidos/estado/<str:estado>/', views_dam.pedidos_por_estado, name='pedidos-por-estado'),
    path('pedidos/<int:pedido_id>/estado/<str:estado>/', views_dam.actualizar_estado_pedido, name='actualizar-estado-pedido'),
    
    # Endpoints de carrito
    path('usuario/<int:usuario_id>/carrito/', views_dam.añadir_al_carrito, name='añadir-al-carrito'),
    path('usuario/<int:usuario_id>/carrito/<int:producto_id>/', views_dam.borrar_del_carrito, name='borrar-del-carrito'),
]
