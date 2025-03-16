from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet
# Router
router = DefaultRouter()
router.register(r'', ClassViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]
