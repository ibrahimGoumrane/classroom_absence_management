from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet , AttendanceProcessView, AttendanceConfirmView, GenerateEncodingsView, get_teacher_attendance_last_30_days
# Router
router = DefaultRouter()
router.register(r'', AttendanceViewSet)

# URLs
urlpatterns = [
    path('process/', AttendanceProcessView.as_view({'post': 'post'}), name='process'),
    path('generate/', GenerateEncodingsView.as_view({'post': 'post'}), name='generate'),
    path('confirm/', AttendanceConfirmView.as_view({'post': 'post'}), name='confirm'),
    path('attendance-last-30-days/teacher/<int:id>/', get_teacher_attendance_last_30_days, name='attendance-last-30-days-teacher'),
    path('', include(router.urls)),
]
