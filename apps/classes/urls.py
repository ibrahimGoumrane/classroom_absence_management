from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet
from apps.classes.views import  get_class_attendance , get_class_subjects
# Router
router = DefaultRouter()
router.register(r'', ClassViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/attendance/', get_class_attendance, name='class-attendance'),
    path('<int:id>/subjects/', get_class_subjects, name='class-subjects'),
]
