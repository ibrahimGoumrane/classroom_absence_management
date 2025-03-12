from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet , AttendanceProcessView, AttendanceConfirmView
# Router
router = DefaultRouter()
router.register(r'', AttendanceViewSet)

# URLs
urlpatterns = [
    path('process/', AttendanceProcessView.as_view({'get': 'get'}), name='process'),
    path('confirm/', AttendanceConfirmView.as_view({'post': 'post'}), name='confirm'),
]
