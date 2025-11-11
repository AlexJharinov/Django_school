from rest_framework import generics, permissions, viewsets

from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwnerOrModerator
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD по курсам.
    - Модераторы: могут смотреть и редактировать, но не создавать и не удалять.
    - Владельцы: могут работать только со своими курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """При создании автоматически проставляем владельца."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            # Модератор видит все курсы
            return Course.objects.all()
        # Остальные — только свои
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        # Запрещаем модератору POST и DELETE
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="Модераторы").exists():
            if self.action in ["create", "destroy"]:
                self.permission_classes = [
                    permissions.IsAdminUser
                ]  # запретит модераторам
            elif self.action in ["update", "partial_update", "list", "retrieve"]:
                self.permission_classes = [
                    permissions.IsAuthenticated,
                    IsOwnerOrModerator,
                ]
        else:
            # Обычные пользователи
            if self.action in ["list", "retrieve"]:
                self.permission_classes = [permissions.IsAuthenticated]
            elif self.action in ["update", "partial_update", "destroy", "create"]:
                self.permission_classes = [
                    permissions.IsAuthenticated,
                    IsOwnerOrModerator,
                ]

        return [perm() for perm in self.permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    """
    Список и создание уроков.
    Модератор — только просмотр.
    Владельцы — могут создавать.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="Модераторы").exists():
            # Модератору запрещаем POST
            if self.request.method == "POST":
                self.permission_classes = [permissions.IsAdminUser]  # запрет
            else:
                self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in self.permission_classes]


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование, удаление урока.
    Модератор — только просмотр и редактирование.
    Владельцы — всё со своими.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="Модераторы").exists():
            if self.request.method == "DELETE":
                self.permission_classes = [permissions.IsAdminUser]  # запретить
            else:
                self.permission_classes = [
                    permissions.IsAuthenticated,
                    IsOwnerOrModerator,
                ]
        else:
            self.permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerOrModerator,
            ]
        return [perm() for perm in self.permission_classes]
