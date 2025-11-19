from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        required=False,
        validators=[validate_youtube_url],
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "video_url",
            "course",
            "owner",
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # вложенные уроки
    lessons_count = serializers.SerializerMethodField()  # количество уроков

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с курсом"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Проверяем, подписан ли текущий пользователь на курс.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
