from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet ,LoginView ,SignupView , LogoutView

# Router for User CRUD
router = DefaultRouter()
router.register(r'', UserViewSet)


# URLs
urlpatterns = [
    path('users/', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),  # Separate path for SignupView
    path('login/', LoginView.as_view(), name='login'),  # Separate path for LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Separate path for LogoutView
]