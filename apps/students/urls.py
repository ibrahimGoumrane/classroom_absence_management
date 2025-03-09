from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UploadStudentImagesView
# Router
router = DefaultRouter()
router.register(r'', StudentViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('api/folder/images', UploadStudentImagesView.as_view(), name='upload-images'),
]
