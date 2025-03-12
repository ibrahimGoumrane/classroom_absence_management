from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet
# Router
router = DefaultRouter()
router.register(r'', AttendanceViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]
