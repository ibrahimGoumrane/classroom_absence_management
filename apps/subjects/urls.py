from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet
# Router
router = DefaultRouter()
router.register(r'', SubjectViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]