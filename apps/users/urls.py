from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet ,LoginView ,SignupView

# Router for User CRUD
router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'login', LoginView)
router.register(r'signup', SignupView)


# URLs
urlpatterns = [
    path('', include(router.urls)),
]