from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
# Router
router = DefaultRouter()
router.register(r'', UserViewSet)

# URLs
urlpatterns = [
    path('/', include(router.urls)),
]