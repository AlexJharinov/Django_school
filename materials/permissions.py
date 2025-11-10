from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверяет, что пользователь принадлежит к группе 'Модераторы'.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()


        )

class IsModerator(BasePermission):
    """
    Проверяет, что пользователь состоит в группе 'Модераторы'.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsOwnerOrModerator(BasePermission):
    """
    Разрешает доступ модераторам ко всем объектам.
    Обычным пользователям — только к своим.
    """

    def has_object_permission(self, request, view, obj):
        # Модератор может всё, кроме create/delete (ограничим во вьюхе)
        if request.user.groups.filter(name="Модераторы").exists():
            return True
        # Иначе разрешаем доступ только владельцу объекта
        return obj.owner == request.user