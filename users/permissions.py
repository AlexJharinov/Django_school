from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSelfOrAdmin(BasePermission):
    """
    Разрешает доступ админу ко всем пользователям,
    а обычному пользователю — только к своему профилю.
    """

    def has_object_permission(self, request, view, obj):
        # Админ может всё
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Пользователь может только у себя
        return obj == request.user
