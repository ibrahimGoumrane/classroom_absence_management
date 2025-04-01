from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet

# Router
router = DefaultRouter()
router.register(r'', DepartmentViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]
