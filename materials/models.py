# from django.contrib.auth.models import User
from django.db import models

from config import settings


class Course(models.Model):
    """
    Модель курса.
    """

    title = models.CharField(max_length=225, verbose_name="Название")
    preview = models.ImageField(
        upload_to="courses/preview",
        blank=True,
        null=True,
        verbose_name="Превью(картинка)",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <— правильная ссылка
        on_delete=models.CASCADE,
        related_name="Владелец_курса",
        null=True,
        blank=True,
    )
    stripe_product_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID продукта в Stripe"
    )
    stripe_price_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID цены в Stripe"
    )

    last_update_at = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока.
    """

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=225, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lessons/preview",
        blank=True,
        null=True,
        verbose_name="Превью(картинка)",
    )
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <— правильная ссылка
        on_delete=models.CASCADE,
        related_name="владелец_урока",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.title} ({self.course.title})"


# from django.conf import settings
# from django.db import models

# class Subscription(models.Model):
#     """
#     Подписка пользователя на курс.
#     """
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="subscriptions",
#         verbose_name="Пользователь",
#     )
#     course = models.ForeignKey(
#         "materials.Course",
#         on_delete=models.CASCADE,
#         related_name="subscriptions",
#         verbose_name="Курс",
#     )
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
#
#     class Meta:
#         unique_together = ("user", "course")  # одна подписка на курс
#         verbose_name = "Подписка"
#         verbose_name_plural = "Подписки"
#
#     def __str__(self):
#         return f"{self.user.email} → {self.course.title}"
