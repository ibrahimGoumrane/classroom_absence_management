from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, get_teacher_subjects_attendance_today
# Router
router = DefaultRouter()
router.register(r'', SubjectViewSet)

# URLs
urlpatterns = [
    path('attendance-today/teacher/<int:id>/', get_teacher_subjects_attendance_today, name='teacher-subjects-attendance-today'),
    path('', include(router.urls)),
]