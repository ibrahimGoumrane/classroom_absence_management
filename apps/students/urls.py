from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet ,get_student_attendance
# Router
router = DefaultRouter()
router.register(r'', StudentViewSet)  # This correctly prefixes student-related endpoints

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/attendances/', get_student_attendance, name='student-attendances'),
]   