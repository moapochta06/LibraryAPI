from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешено получать запросы для любого пользователя
        if request.method in permissions.SAFE_METHODS:  
            return True
        # Разрешено только пользователям с правами администратора выполнять другие методы
        return request.user and request.user.is_staff