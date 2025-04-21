from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F
from .models import Producto, Pedido, DetallePedido, CarritoCompra, DetalleCarrito
from django.shortcuts import get_object_or_404

# Endpoints de Productos (APP MÓVIL - DAM)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productos_vendidos(request):
    """Endpoint de la APP MÓVIL (DAM): Obtiene estadísticas de productos vendidos"""
    productos = Producto.objects.annotate(
        total_vendido=Sum('detallepedido__cantidad'),
        ingresos=Sum(F('detallepedido__cantidad') * F('detallepedido__precio'))
    ).filter(total_vendido__gt=0).order_by('-total_vendido')
    
    return Response([{
        'id': p.id,
        'nombre': p.nombre,
        'cantidad_vendida': p.total_vendido or 0,
        'ingresos': float(p.ingresos or 0)
    } for p in productos])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def producto_mas_vendido(request):
    """Endpoint de la APP MÓVIL (DAM): Obtiene el producto más vendido"""
    producto = Producto.objects.annotate(
        total_vendido=Sum('detallepedido__cantidad')
    ).order_by('-total_vendido').first()
    
    if not producto:
        return Response({'message': 'No hay productos vendidos'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'id': producto.id,
        'nombre': producto.nombre,
        'cantidad_vendida': producto.total_vendido or 0
    })

# Endpoints de Pedidos (APP MÓVIL - DAM)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pedidos_usuario(request, usuario_id):
    """Endpoint de la APP MÓVIL (DAM): Obtiene los pedidos de un usuario"""
    pedidos = Pedido.objects.filter(usuario_id=usuario_id).order_by('-fecha_creacion')
    return Response([{
        'id': p.id,
        'fecha': p.fecha_creacion,
        'estado': p.estado,
        'total': float(p.total_precio),
        'tienda': p.tienda.nombre if p.tienda else None
    } for p in pedidos])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pedidos_por_estado(request, estado):
    """Endpoint de la APP MÓVIL (DAM): Filtra pedidos por estado"""
    if estado not in ['pendiente', 'enviado', 'entregado', 'cancelado']:
        return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
    
    pedidos = Pedido.objects.filter(estado=estado).order_by('-fecha_creacion')
    return Response([{
        'id': p.id,
        'usuario': p.usuario.email,
        'fecha': p.fecha_creacion,
        'total': float(p.total_precio),
        'tienda': p.tienda.nombre if p.tienda else None
    } for p in pedidos])

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_estado_pedido(request, pedido_id, estado):
    """Endpoint de la APP MÓVIL (DAM): Actualiza el estado de un pedido"""
    if estado not in ['pendiente', 'enviado', 'entregado', 'cancelado']:
        return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = estado
    pedido.save()
    
    return Response({
        'id': pedido.id,
        'estado': pedido.estado,
        'mensaje': 'Estado actualizado correctamente'
    })

# Endpoints de Carrito (APP MÓVIL - DAM)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def añadir_al_carrito(request, usuario_id, tienda_id):
    """Endpoint de la APP MÓVIL (DAM): Añade un producto al carrito"""
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)
    
    # Obtener o crear el carrito del usuario
    carrito, _ = CarritoCompra.objects.get_or_create(usuario_id=usuario_id)
    
    # Verificar que el producto existe y pertenece a la tienda
    producto = get_object_or_404(Producto, id=producto_id, tienda_id=tienda_id)
    
    # Verificar stock
    if producto.stock < cantidad:
        return Response({
            'error': 'Stock insuficiente'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Añadir o actualizar item en el carrito
    detalle, created = DetalleCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    if not created:
        detalle.cantidad += cantidad
        detalle.save()
    
    return Response({
        'mensaje': 'Producto añadido al carrito',
        'cantidad': detalle.cantidad
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def borrar_del_carrito(request, usuario_id, producto_id):
    """Endpoint de la APP MÓVIL (DAM): Elimina un producto del carrito"""
    carrito = get_object_or_404(CarritoCompra, usuario_id=usuario_id)
    detalle = get_object_or_404(DetalleCarrito, carrito=carrito, producto_id=producto_id)
    detalle.delete()
    
    return Response({
        'mensaje': 'Producto eliminado del carrito'
    })
