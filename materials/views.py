from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.viewsets import ModelViewSet

from materials import permissions
from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwnerOrModerator
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """
        При создании автоматически проставляем владельца.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            # Модератор видит все курсы
            return Course.objects.all()
        # Остальные — только свои
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        elif self.action == "destroy":
            # Модераторы не могут удалять, только владелец
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
        elif self.action == "create":
            # Модераторы не создают — только владельцы
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in self.permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in self.permission_classes]


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]

