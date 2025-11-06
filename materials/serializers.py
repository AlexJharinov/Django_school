from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # вложенные уроки
    lessons_count = serializers.SerializerMethodField()     # количество уроков

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с курсом"""
        return obj.lessons.count()




