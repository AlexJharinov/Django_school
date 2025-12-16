from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseBuyView, CourseViewSet, LessonDetailView,
                             LessonListCreateView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")  # ← важно указать имя

urlpatterns = [
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    path("courses/<int:pk>/buy/", CourseBuyView.as_view(), name="course-buy"),
]

urlpatterns += router.urls
