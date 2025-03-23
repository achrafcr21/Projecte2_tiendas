from rest_framework import serializers
from .models import Usuario, Tienda, Producto, Pedido, Solicitud, Servicio, TiendaServicio

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'username', 'password', 'rol', 'fecha_registro')
        read_only_fields = ('fecha_registro',)
        extra_kwargs = {
            'rol': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'rol' in validated_data and instance.rol != validated_data['rol']:
            raise serializers.ValidationError("El rol no puede ser modificado después del registro")
        return super().update(instance, validated_data)

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ('id', 'nombre', 'descripcion', 'fecha_registro', 'propietario')
        read_only_fields = ('fecha_registro', 'propietario')  # El propietario se asigna automáticamente

    def create(self, validated_data):
        # El propietario se asigna en la vista, no se debe proporcionar en el payload
        return super().create(validated_data)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'total_precio', 'status')

class SolicitudSerializer(serializers.ModelSerializer):
    """
    Serialitzador per les sol·licituds de digitalització.
    Permet crear sol·licituds (públic) i gestionar-les (admin).
    """
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Solicitud
        fields = [
            'id', 
            'nombre_negocio', 
            'descripcion', 
            'email_contacto', 
            'telefono',
            'fecha_solicitud',
            'estado',
            'estado_display',
            'notas_admin'
        ]
        read_only_fields = ['fecha_solicitud']
        extra_kwargs = {
            'nombre_negocio': {'required': False},
            'descripcion': {'required': False},
            'email_contacto': {'required': False},
            'telefono': {'required': False}
        }

    def to_representation(self, instance):
        """
        Modifica la representació segons si l'usuari és admin o no
        """
        ret = super().to_representation(instance)
        request = self.context.get('request')
        
        # Si no hi ha request o l'usuari no és admin, eliminem les notes
        if not request or not request.user or request.user.rol != 'admin':
            ret.pop('notas_admin', None)
        
        return ret

class ServicioSerializer(serializers.ModelSerializer):
    """
    Serialitzador pels serveis disponibles.
    Mostra tots els camps pels admins, però oculta 'activo' pels clients.
    """
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'activo']
        read_only_fields = ['id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        
        # Si no és admin, no mostrem els serveis inactius
        if not request or not request.user or request.user.rol != 'admin':
            if not ret.get('activo', True):
                raise serializers.ValidationError("Aquest servei no està disponible")
            ret.pop('activo', None)
        
        return ret

class TiendaServicioSerializer(serializers.ModelSerializer):
    """
    Serialitzador per la relació entre botigues i serveis.
    Inclou informació detallada del servei.
    """
    servicio = ServicioSerializer(read_only=True)
    servicio_id = serializers.PrimaryKeyRelatedField(
        queryset=Servicio.objects.filter(activo=True),
        write_only=True,
        source='servicio'
    )
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = TiendaServicio
        fields = [
            'id', 
            'tienda', 
            'servicio',
            'servicio_id',
            'estado',
            'estado_display',
            'fecha_contratacion',
            'notas',
            'precio_final'
        ]
        read_only_fields = ['id', 'tienda', 'fecha_contratacion']

    def validate(self, data):
        # Verificar que el servei està actiu
        if not data['servicio'].activo:
            raise serializers.ValidationError(
                "No es pot assignar un servei inactiu"
            )
        
        # Verificar que la botiga no té ja aquest servei
        tienda = self.context['tienda']
        if TiendaServicio.objects.filter(
            tienda=tienda, 
            servicio=data['servicio']
        ).exists():
            raise serializers.ValidationError(
                "Aquesta botiga ja té aquest servei assignat"
            )
        
        # Assignar el preu base com a preu final per defecte
        if 'precio_final' not in data:
            data['precio_final'] = data['servicio'].precio
        
        return data

    def create(self, validated_data):
        # Assignar la botiga del context
        validated_data['tienda'] = self.context['tienda']
        return super().create(validated_data)
