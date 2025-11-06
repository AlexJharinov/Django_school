from django.core.management.base import BaseCommand
from users.models import Payment
from materials.models import Course, Lesson
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Создаёт тестовые данные для платежей"

    def handle(self, *args, **options):
        User = get_user_model()

        # Проверяем, есть ли пользователь
        user1 = User.objects.first()
        if not user1:
            user1 = User.objects.create_user(
                email="test@example.com",
                password="1234"
            )
            self.stdout.write(self.style.WARNING("⚠️ Создан тестовый пользователь test@example.com"))

        # Берём первый курс и урок
        course1 = Course.objects.first()
        lesson1 = Lesson.objects.first()

        # Создаём платежи
        Payment.objects.create(
            user=user1,
            paid_course=course1,
            amount=1500,
            payment_method='transfer'
        )

        Payment.objects.create(
            user=user1,
            paid_lesson=lesson1,
            amount=300,
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS("Платежи добавлены"))
