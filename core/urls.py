from django.urls import path
from .views import registro_usuario  # Asegurar que esta vista existe

app_name = 'core'

urlpatterns = [
    path('api/registro/', registro_usuario, name='registro_usuario'),
]