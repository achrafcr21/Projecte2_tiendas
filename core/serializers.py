from rest_framework import serializers
from .models import Usuario, Tienda, Producto, Pedido

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
        read_only_fields = ('fecha_registro',)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'total_precio', 'status')
