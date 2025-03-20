from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permís personalitzat per comprovar si l'usuari és administrador
    """
    def has_permission(self, request, view):
        # Permet GET a qualsevol usuari autenticat
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Per POST, PUT, DELETE: només usuaris admin
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

    def has_object_permission(self, request, view, obj):
        # Permet GET a qualsevol usuari autenticat
        if request.method in permissions.SAFE_METHODS:
            return True
        # Només el propietari pot modificar o eliminar la tienda
        return obj.propietario == request.user
