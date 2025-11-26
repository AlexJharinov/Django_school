from rest_framework import generics, permissions, viewsets, status
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwnerOrModerator
from materials.serializers import CourseSerializer, LessonSerializer
from materials.services import create_checkout_session_for_course
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from users.models import Subscription
from materials.tasks import send_course_update_email


from datetime import timedelta
from django.utils import timezone

from users.models import Subscription
from materials.tasks import send_course_update_email


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
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        user = self.request.user

        if user.is_authenticated and user.groups.filter(name="Модераторы").exists():
            if self.action in ["create", "destroy"]:
                # Модератора режем по созданию/удалению
                self.permission_classes = [permissions.IsAdminUser]
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

    def perform_update(self, serializer):
        # 1. Берём курс до сохранения, чтобы запомнить прошлое время обновления
        course_before = self.get_object()
        previous_updated_at = course_before.last_update_at

        # 2. Сохраняем изменения
        course = serializer.save()

        now = timezone.now()

        # 3. Если курс обновлялся менее 4 часов назад — уведомления не шлём
        if previous_updated_at and (now - previous_updated_at) < timedelta(hours=4):
            return

        # 4. Шлём письма всем подписчикам этого курса
        subscriptions = Subscription.objects.filter(course=course).select_related("user")

        for sub in subscriptions:
            email = sub.user.email
            if email:
                send_course_update_email.delay(email, course.title)



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

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        now = timezone.now()

        if course.last_update_at and (now - course.last_update_at) < timedelta(hours=4):
            return

        subs = course.subscriptions.all()
        for sub in subs:
            send_course_update_email.delay(sub.user.email, course.title)

        # обновим timestamp у курса
        course.last_update_at = now
        course.save(update_fields=["last_update_at"])

class CourseBuyView(APIView):
    """
    Создаёт Stripe Checkout Session для оплаты курса и возвращает ссылку.
    """
    permission_classes = [permissions.IsAuthenticated]  # или AllowAny, как у тебя в проекте

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        session = create_checkout_session_for_course(course, user=request.user)

        return Response(
            {"checkout_url": session.url},
            status=status.HTTP_201_CREATED,
        )