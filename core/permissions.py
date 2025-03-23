from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permet l'accés només a usuaris admin.
    Per a objectes específics, verifica que l'usuari sigui el propietari.
    """
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'admin'

    def has_object_permission(self, request, view, obj):
        return obj.propietario == request.user

class IsAdmin(permissions.BasePermission):
    """
    Permet l'accés només a usuaris admin.
    No verifica propietat d'objectes.
    """
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.rol == 'admin'
