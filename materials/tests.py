from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Lesson

User = get_user_model()


class LessonCRUDTestCase(APITestCase):
    """
    Тестирование CRUD операций для уроков.
    """

    def setUp(self):
        # Создаём тестовых пользователей
        self.user = User.objects.create_user(email="user@example.com", password="12345")
        self.moderator = User.objects.create_user(
            email="mod@example.com", password="12345"
        )
        # Назначим модератору группу "Модераторы", если есть
        self.moderator.groups.create(name="Модераторы")

        # Создаём тестовый курс и урок
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            description="Description",
            course=self.course,
            owner=self.user,
        )

        # API клиент
        self.client = APIClient()

    def test_list_lessons_authenticated(self):
        """Авторизованный пользователь получает список уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_create_lesson(self):
        """Создание урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Lesson",
            "description": "Test description",
            "course": self.course.id,
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson_owner(self):
        """Обновление урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Updated Title"}
        response = self.client.patch(f"/api/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Title")

    def test_delete_lesson_not_owner(self):
        """Удаление урока другим пользователем запрещено"""
        other_user = User.objects.create_user(
            email="other@example.com", password="12345"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class SubscriptionTestCase(APITestCase):
#     """
#     Тестирование подписки/отписки на курс.
#     """
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="sub@example.com", password="12345"
#         )
#         self.course = Course.objects.create(title="Sub Course", owner=self.user)
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_subscribe_and_unsubscribe(self):
#         """Пользователь может подписаться и отписаться от курса"""
#         url = "/api/subscriptions/"
#         data = {"course_id": self.course.id}
#
#         # Подписка
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
#
#         # Повторный вызов — отписка
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
