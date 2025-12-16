from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter

# from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.permissions import IsSelfOrAdmin
from users.serializers import PaymentSerializer, UserCreateSerializer, UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # сортировка по умолчанию (новые сверху)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Полный CRUD по пользователю.
    - Админ: видит и редактирует всех пользователей.
    - Пользователь: может видеть и изменять только себя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        # обычный пользователь видит только себя
        return User.objects.filter(id=user.id)

    def perform_destroy(self, instance):
        # разрешаем удалить только себя (или админом)
        if instance == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Вы можете удалить только свой аккаунт.")


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации нового пользователя (без токена).
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
