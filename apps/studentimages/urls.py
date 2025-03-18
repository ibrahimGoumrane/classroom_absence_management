from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadStudentImagesView
# Router
router = DefaultRouter()
router.register(r'', UploadStudentImagesView, basename="student-images")  # Fix images URL

# URLs
urlpatterns = [
    path('', include(router.urls)),  
]