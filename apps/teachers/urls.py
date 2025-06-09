from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet , get_teacher_attendance ,get_teacher_subjects, get_teacher_total_students, get_teacher_total_subjects
# Router
router = DefaultRouter()
router.register(r'', TeacherViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/subjects/', get_teacher_subjects, name='teacher-subjects'),
    path('<int:id>/attendance/', get_teacher_attendance, name='teacher-attendance'),
    path('<int:id>/total/students/', get_teacher_total_students, name='teacher-total-students'),
    path('<int:id>/total/subjects/', get_teacher_total_subjects, name='teacher-total-subjects'),
    path('<int:id>/total/classes/', get_teacher_total_subjects, name='teacher-total-classes'),
]
