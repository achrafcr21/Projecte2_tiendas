from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Count, Sum, F
from .models import Producto, Pedido, DetallePedido, CarritoCompra, DetalleCarrito, Tienda
from django.shortcuts import get_object_or_404

# Endpoints de Productos (APP MÓVIL - DAM)

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_productos(request):
    """Endpoint de la APP MÓVIL (DAM): Lista todos los productos disponibles"""
    # Obtener parámetros de filtrado
    tienda_id = request.query_params.get('tienda', None)
    categoria = request.query_params.get('categoria', None)
    
    # Consulta base
    productos = Producto.objects.all()
    
    # Aplicar filtros si existen
    if tienda_id:
        productos = productos.filter(tienda_id=tienda_id)
    if categoria:
        productos = productos.filter(categoria=categoria)
    
    # Devolver lista de productos
    return Response([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'precio': float(p.precio),
        'stock': p.stock,
        'categoria': p.categoria,
        'tienda_id': p.tienda_id
    } for p in productos])

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def producto_detalle(request, producto_id):
    """
    Endpoint de la APP MÓVIL (DAM): 
    GET: Obtiene los detalles de un producto específico
    PUT: Modifica un producto existente (solo propietario de la tienda)
    DELETE: Elimina un producto (solo propietario de la tienda)
    """
    try:
        producto = Producto.objects.get(id=producto_id)
        
        # Para PUT y DELETE, verificar que el usuario es propietario de la tienda
        if request.method in ['PUT', 'DELETE']:
            if not producto.tienda or producto.tienda.propietario != request.user:
                return Response(
                    {'error': 'No tienes permiso para modificar este producto'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        if request.method == 'GET':
            return Response({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': float(producto.precio),
                'stock': producto.stock,
                'categoria': producto.categoria,
                'tienda_id': producto.tienda_id
            })
            
        elif request.method == 'PUT':
            # Actualizar campos permitidos
            producto.nombre = request.data.get('nombre', producto.nombre)
            producto.descripcion = request.data.get('descripcion', producto.descripcion)
            producto.precio = request.data.get('precio', producto.precio)
            producto.stock = request.data.get('stock', producto.stock)
            producto.categoria = request.data.get('categoria', producto.categoria)
            producto.save()
            
            return Response({
                'mensaje': 'Producto actualizado correctamente',
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': float(producto.precio),
                'stock': producto.stock,
                'categoria': producto.categoria,
                'tienda_id': producto.tienda_id
            })
            
        elif request.method == 'DELETE':
            producto.delete()
            return Response(
                {'mensaje': 'Producto eliminado correctamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_producto(request):
    """
    Endpoint de la APP MÓVIL (DAM): Crea un nuevo producto
    Solo el propietario de una tienda puede crear productos para su tienda
    """
    tienda_id = request.data.get('tienda_id')
    if not tienda_id:
        return Response(
            {'error': 'Se requiere especificar una tienda'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar que el usuario es propietario de la tienda
    tienda = get_object_or_404(Tienda, id=tienda_id)
    if tienda.propietario != request.user:
        return Response(
            {'error': 'No tienes permiso para crear productos en esta tienda'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        producto = Producto.objects.create(
            nombre=request.data['nombre'],
            descripcion=request.data.get('descripcion', ''),
            precio=request.data['precio'],
            stock=request.data.get('stock', 0),
            categoria=request.data.get('categoria'),
            tienda=tienda
        )
        
        return Response({
            'mensaje': 'Producto creado correctamente',
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'stock': producto.stock,
            'categoria': producto.categoria,
            'tienda_id': producto.tienda_id
        }, status=status.HTTP_201_CREATED)
        
    except KeyError as e:
        return Response(
            {'error': f'Falta el campo requerido: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_pedido(request, pedido_id):
    """Endpoint de la APP MÓVIL (DAM): Obtiene los detalles completos de un pedido"""
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Solo el propietario de la tienda o el usuario que hizo el pedido pueden verlo
        if pedido.usuario != request.user and (not pedido.tienda or pedido.tienda.propietario != request.user):
            return Response(
                {'error': 'No tienes permiso para ver este pedido'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener los detalles del pedido
        detalles = DetallePedido.objects.filter(pedido=pedido)
        
        return Response({
            'id': pedido.id,
            'usuario': {
                'id': pedido.usuario.id,
                'email': pedido.usuario.email
            },
            'tienda': {
                'id': pedido.tienda.id,
                'nombre': pedido.tienda.nombre
            } if pedido.tienda else None,
            'total_precio': float(pedido.total_precio),
            'estado': pedido.estado,
            'fecha_creacion': pedido.fecha_creacion,
            'detalles': [{
                'producto': {
                    'id': detalle.producto.id,
                    'nombre': detalle.producto.nombre,
                    'precio': float(detalle.precio)
                },
                'cantidad': detalle.cantidad,
                'subtotal': float(detalle.precio * detalle.cantidad)
            } for detalle in detalles]
        })
        
    except Pedido.DoesNotExist:
        return Response(
            {'error': 'Pedido no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ultimos_cinco_pedidos(request):
    """Endpoint de la APP MÓVIL (DAM): Obtiene los últimos 5 pedidos de la tienda del usuario"""
    # Verificar que el usuario tiene una tienda
    tienda = Tienda.objects.filter(propietario=request.user).first()
    if not tienda:
        return Response(
            {'error': 'No tienes una tienda asociada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Obtener los últimos 5 pedidos
    pedidos = Pedido.objects.filter(tienda=tienda).order_by('-fecha_creacion')[:5]
    
    return Response([{
        'id': pedido.id,
        'usuario': {
            'id': pedido.usuario.id,
            'email': pedido.usuario.email
        },
        'total_precio': float(pedido.total_precio),
        'estado': pedido.estado,
        'fecha_creacion': pedido.fecha_creacion
    } for pedido in pedidos])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todos_los_pedidos(request):
    """Endpoint de la APP MÓVIL (DAM): Obtiene todos los pedidos de la tienda del usuario"""
    # Verificar que el usuario tiene una tienda
    tienda = Tienda.objects.filter(propietario=request.user).first()
    if not tienda:
        return Response(
            {'error': 'No tienes una tienda asociada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Obtener todos los pedidos
    pedidos = Pedido.objects.filter(tienda=tienda).order_by('-fecha_creacion')
    
    return Response([{
        'id': pedido.id,
        'usuario': {
            'id': pedido.usuario.id,
            'email': pedido.usuario.email
        },
        'total_precio': float(pedido.total_precio),
        'estado': pedido.estado,
        'fecha_creacion': pedido.fecha_creacion
    } for pedido in pedidos])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_pedido(request, pedido_id):
    """
    Endpoint de la APP MÓVIL (DAM): Ver detalles de un pedido específico
    """
    try:
        # Obtener el pedido y verificar que pertenece al usuario
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        if pedido.usuario_id != request.user.id:
            return Response(
                {'error': 'No tienes permiso para ver este pedido'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Obtener los detalles del pedido
        detalles = DetallePedido.objects.filter(pedido=pedido).select_related('producto')
        
        return Response({
            'id': pedido.id,
            'fecha': pedido.fecha_creacion,
            'estado': pedido.estado,
            'productos': [{
                'id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'precio': float(detalle.precio),
                'cantidad': detalle.cantidad,
                'subtotal': float(detalle.precio * detalle.cantidad)
            } for detalle in detalles],
            'total': float(pedido.total_precio)
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pedidos(request):
    """
    Endpoint de la APP MÓVIL (DAM): Listar todos los pedidos del usuario
    """
    try:
        # Obtener todos los pedidos del usuario
        pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        
        return Response([{
            'id': pedido.id,
            'fecha': pedido.fecha_creacion,
            'estado': pedido.estado,
            'total': float(pedido.total_precio)
        } for pedido in pedidos])
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_carrito(request, usuario_id):
    """
    Endpoint de la APP MÓVIL (DAM): Obtiene el contenido del carrito de un usuario
    """
    try:
        # Verificar que el usuario autenticado es el dueño del carrito
        if request.user.id != usuario_id:
            return Response(
                {'error': 'No tienes permiso para ver este carrito'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Obtener o crear el carrito del usuario
        carrito, created = CarritoCompra.objects.get_or_create(usuario_id=usuario_id)
        
        # Obtener los detalles del carrito
        detalles = DetalleCarrito.objects.filter(carrito=carrito).select_related('producto')
        
        # Calcular el total
        total = sum(detalle.producto.precio * detalle.cantidad for detalle in detalles)
        
        return Response({
            'id': carrito.id,
            'productos': [{
                'id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'precio': float(detalle.producto.precio),
                'cantidad': detalle.cantidad,
                'subtotal': float(detalle.producto.precio * detalle.cantidad)
            } for detalle in detalles],
            'total': float(total)
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_cantidad_carrito(request, usuario_id, producto_id):
    """
    Endpoint de la APP MÓVIL (DAM): Actualiza la cantidad de un producto en el carrito
    """
    try:
        # Verificar que el usuario autenticado es el dueño del carrito
        if request.user.id != usuario_id:
            return Response(
                {'error': 'No tienes permiso para modificar este carrito'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        cantidad = request.data.get('cantidad', 0)
        if cantidad < 0:
            return Response(
                {'error': 'La cantidad debe ser mayor o igual a 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        carrito = CarritoCompra.objects.get(usuario_id=usuario_id)
        detalle = DetalleCarrito.objects.get(carrito=carrito, producto_id=producto_id)
        
        if cantidad == 0:
            detalle.delete()
            mensaje = 'Producto eliminado del carrito'
        else:
            detalle.cantidad = cantidad
            detalle.save()
            mensaje = 'Cantidad actualizada correctamente'
            
        return Response({'mensaje': mensaje})
        
    except CarritoCompra.DoesNotExist:
        return Response(
            {'error': 'Carrito no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except DetalleCarrito.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado en el carrito'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def vaciar_carrito(request, usuario_id):
    """
    Endpoint de la APP MÓVIL (DAM): Elimina todos los productos del carrito
    """
    try:
        # Verificar que el usuario autenticado es el dueño del carrito
        if request.user.id != usuario_id:
            return Response(
                {'error': 'No tienes permiso para vaciar este carrito'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        carrito = CarritoCompra.objects.get(usuario_id=usuario_id)
        DetalleCarrito.objects.filter(carrito=carrito).delete()
        
        return Response({'mensaje': 'Carrito vaciado correctamente'})
        
    except CarritoCompra.DoesNotExist:
        return Response(
            {'error': 'Carrito no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pedido_desde_carrito(request, usuario_id):
    """
    Endpoint de la APP MÓVIL (DAM): Convierte el carrito actual en un pedido
    """
    try:
        # Verificar que el usuario autenticado es el dueño del carrito
        if request.user.id != usuario_id:
            return Response(
                {'error': 'No tienes permiso para crear un pedido con este carrito'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        carrito = CarritoCompra.objects.get(usuario_id=usuario_id)
        detalles = DetalleCarrito.objects.filter(carrito=carrito).select_related('producto')
        
        if not detalles.exists():
            return Response(
                {'error': 'El carrito está vacío'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Calcular el total del pedido
        total = sum(detalle.producto.precio * detalle.cantidad for detalle in detalles)
        
        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario_id=usuario_id,
            total_precio=total,
            estado='pendiente'
        )
        
        # Crear los detalles del pedido
        for detalle in detalles:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=detalle.producto,
                cantidad=detalle.cantidad,
                precio=detalle.producto.precio
            )
            
        # Vaciar el carrito
        detalles.delete()
        
        return Response({
            'mensaje': 'Pedido creado correctamente',
            'pedido_id': pedido.id,
            'total': float(total)
        }, status=status.HTTP_201_CREATED)
        
    except CarritoCompra.DoesNotExist:
        return Response(
            {'error': 'Carrito no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
