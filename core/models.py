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
    """
    Model pels serveis que oferim als clients.
    Per exemple: web, app, marketing digital, etc.
    """
    nombre = models.CharField(max_length=200, verbose_name='Nom')
    descripcion = models.TextField(
        verbose_name='Descripció',
        blank=True,  # Permitir campo vacío en formularios
        null=True    # Permitir NULL en la base de datos
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Preu base'
    )
    activo = models.BooleanField(default=True, verbose_name='Actiu')
    
    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servei'
        verbose_name_plural = 'Serveis'

    def __str__(self):
        return self.nombre

class TiendaServicio(models.Model):
    """
    Model per la relació entre botigues i serveis.
    Guarda l'estat del servei per cada botiga.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendent d\'iniciar'),
        ('en_proceso', 'En procés'),
        ('completado', 'Completat'),
        ('pausado', 'Pausat')
    ]
    
    tienda = models.ForeignKey(
        Tienda, 
        on_delete=models.CASCADE,
        related_name='servicios',
        verbose_name='Botiga'
    )
    servicio = models.ForeignKey(
        Servicio, 
        on_delete=models.CASCADE,
        verbose_name='Servei'
    )
    estado = models.CharField(
        max_length=50, 
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estat'
    )
    fecha_contratacion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de contractació'
    )
    notas = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Notes de progrés'
    )
    precio_final = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Preu final',
        help_text='Pot variar del preu base segons personalitzacions',
        null=True,  # Permitir NULL temporalmente para la migración
        blank=True  # Permitir campo vacío en formularios
    )

    class Meta:
        db_table = 'tiendas_servicios'
        verbose_name = 'Servei contractat'
        verbose_name_plural = 'Serveis contractats'
        unique_together = ['tienda', 'servicio']  # Una botiga no pot tenir el mateix servei dues vegades

    def __str__(self):
        return f"{self.tienda.nombre} - {self.servicio.nombre} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        # Si no hay precio final, usar el precio base del servicio
        if not self.precio_final and self.servicio:
            self.precio_final = self.servicio.precio
        super().save(*args, **kwargs)

class Proyecto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'proyectos'

class Pago(models.Model):
    """
    Model per gestionar els pagaments dels serveis
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendent'),
        ('completado', 'Completat'),
        ('cancelado', 'Cancel·lat')
    ]
    
    tienda_servicio = models.ForeignKey(
        TiendaServicio,
        on_delete=models.CASCADE,
        related_name='pagos',
        null=True  # Permitimos null temporalmente para la migración
    )
    metodo_pago = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    fecha_pago = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pagos'

    def __str__(self):
        return f"Pago {self.id} - {self.tienda_servicio}"

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
    """
    Model pels tickets de suport dels clients
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendent'),
        ('en_proceso', 'En procés'),
        ('resuelto', 'Resolt')
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    respuesta = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'soporte'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Ticket {self.id} - {self.usuario.username} - {self.asunto}"

class Solicitud(models.Model):
    """
    Model per gestionar les sol·licituds de digitalització de botigues.
    Els clients potencials envien sol·licituds i els admins les gestionen.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada')
    ]
    
    nombre_negocio = models.CharField(max_length=200, verbose_name='Nom del negoci')
    descripcion = models.TextField(verbose_name='Descripció del negoci')
    email_contacto = models.EmailField(verbose_name='Email de contacte')
    telefono = models.CharField(max_length=20, verbose_name='Telèfon')
    fecha_solicitud = models.DateTimeField(default=timezone.now, verbose_name='Data de sol·licitud')
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente',
        verbose_name='Estat'
    )
    notas_admin = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Notes del admin'
    )
    
    class Meta:
        db_table = 'solicitudes'
        ordering = ['-fecha_solicitud']  # Les més recents primer
        verbose_name = 'Sol·licitud'
        verbose_name_plural = 'Sol·licituds'

    def __str__(self):
        return f"{self.nombre_negocio} - {self.get_estado_display()}"