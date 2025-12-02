from django.utils import timezone

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        subject=f"Обновление курса: {course_title}",
        message=f"Привет! В курсе '{course_title}' появилось обновление 🎓",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )