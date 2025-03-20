from django.urls import path
from .views import RegistroUsuarioView, login_view, TiendaListCreateView, TiendaDetailView

app_name = 'core'

urlpatterns = [
    path('api/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api/login/', login_view, name='login'),
    path('api/tiendas/', TiendaListCreateView.as_view(), name='tiendas'),
    path('api/tiendas/<int:pk>/', TiendaDetailView.as_view(), name='tienda-detail'),
]