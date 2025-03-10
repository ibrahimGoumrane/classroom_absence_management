from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UploadStudentImagesView
# Router
router = DefaultRouter()
router.register(r'', StudentViewSet)
router.register(r'images', UploadStudentImagesView)

# URLs
urlpatterns = [
    path('', include(router.urls)),
]
