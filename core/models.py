from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        return self.create_user(email, username, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    rol = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'usuarios'

class Tienda(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_registro = models.DateTimeField(default=timezone.now)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tiendas')

    class Meta:
        db_table = 'tiendas'

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'servicios'

class TiendaServicio(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'tiendas_servicios'

class Proyecto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'proyectos'

class Pago(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pagos'

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'productos'

class CarritoCompra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'carrito_compras'

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'detalle_carrito'

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total_precio = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'pedidos'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedidos'

class Soporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'soporte'