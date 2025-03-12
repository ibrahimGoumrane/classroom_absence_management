from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
# Router
router = DefaultRouter()
router.register(r'', TeacherViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]