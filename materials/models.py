from django.db import models

class Course(models.Model):
    """
    Модель курса.
    """
    title = models.CharField(max_length=225, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/preview", blank=True, null=True, verbose_name="Превью(картинка)" )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    title = models.CharField(max_length=225, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/preview", blank=True, null=True, verbose_name="Превью(картинка)")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.title} ({self.course.title})"
