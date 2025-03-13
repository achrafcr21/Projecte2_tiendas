from django.contrib import admin
from .models import Usuario  # Importa tu modelo de usuario

admin.site.register(Usuario)  # Registra el modelo en el panel de administración