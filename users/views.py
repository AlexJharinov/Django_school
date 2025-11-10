# users/views.py

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]


    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # сортировка по умолчанию (новые сверху)

