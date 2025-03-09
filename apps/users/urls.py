from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FolderCreateView

# Router for User CRUD
router = DefaultRouter()
router.register(r'', UserViewSet)

# URLs
urlpatterns = [
    path('', include(router.urls)),
    path('api/folder', FolderCreateView.as_view(), name='folder-create'),
]