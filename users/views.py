# users/views.py
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from users.models import Payment
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
    CRUD для пользователей.
    Только для авторизованных.
    Можно дополнительно ограничить доступ правами.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # если хочешь, можно ограничить только админам:
    # permission_classes = [permissions.IsAdminUser]


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации нового пользователя.
    Доступен без авторизации.
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]



