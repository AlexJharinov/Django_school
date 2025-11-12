from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра/обновления пользователя (без пароля).
    """

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "is_active")
        read_only_fields = ("id", "is_active")


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.
    Пароль делаем write_only и хэшируем через set_password().
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
