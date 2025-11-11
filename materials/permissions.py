from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    """Проверяет, состоит ли пользователь в группе 'Модераторы'."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsOwnerOrModerator(BasePermission):
    """Модератор — доступ ко всем объектам, пользователь — только к своим."""

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Модераторы").exists():
            return True
        return obj.owner == request.user


class ModeratorNoCreateDelete(BasePermission):
    """
    Запрещает модератору создавать и удалять объекты (POST, DELETE).
    Остальные методы доступны.
    """

    def has_permission(self, request, view):
        is_mod = (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )
        # запрещаем создание и удаление модератору
        if request.method in ("POST", "DELETE") and is_mod:
            return False
        return True
