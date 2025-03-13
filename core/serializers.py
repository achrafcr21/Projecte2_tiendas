from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'password2', 'rol']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from data
        password = validated_data.pop('password')  # Remove password to handle it separately
        
        # Crear usuario usando create_user
        user = Usuario.objects.create_user(
            email=validated_data.pop('email'),
            username=validated_data.pop('username'),
            password=password,
            **validated_data
        )
        return user