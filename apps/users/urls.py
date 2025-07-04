from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrentUserTeacherView, CurrentUserStudentView, UserViewSet, LoginView, SignupView, LogoutView, CurrentUserView

# Router for User CRUD
router = DefaultRouter()
router.register(r'', UserViewSet)


# URLs
urlpatterns = [
    path('users/', include(router.urls)),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('user/teacher/', CurrentUserTeacherView.as_view(), name='current-user-teacher'),
    path('user/student/', CurrentUserStudentView.as_view(), name='current-user-student'),
    path('signup/', SignupView.as_view(), name='signup'),  # Separate path for SignupView
    path('login/', LoginView.as_view(), name='login'),  # Separate path for LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Separate path for LogoutView
]
