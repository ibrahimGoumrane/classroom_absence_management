from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Class
from .serializer import ClassSerializer
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
import shutil

# Create your views here.
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    # Default create method is overridden to create a folder with the class name
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        class_name = response.data.get('name')
        folder_path = os.path.join(settings.MEDIA_ROOT, class_name)
        os.makedirs(folder_path, exist_ok=True)
        return response

    # Default update method is overridden to update the folder name plus the class name
    def update(self, request, *args, **kwargs):
        class_instance = self.get_object()
        class_name = request.data.get('name')
        
        #Here instead of creating new folder, we will update the folder name
        old_class_name = class_instance.name
        old_folder_path = os.path.join(settings.MEDIA_ROOT, old_class_name)
        new_folder_path = os.path.join(settings.MEDIA_ROOT, class_name)
        print(old_folder_path, new_folder_path)
        os.rename(old_folder_path, new_folder_path)
        response = super().update(request, *args, **kwargs)
        return response
    
    # Default destroy method is overridden to delete the folder
    def destroy(self, request, *args, **kwargs):
        class_instance = self.get_object()
        folder_path = os.path.join(settings.MEDIA_ROOT, class_instance.name)
        shutil.rmtree(folder_path)
        return super().destroy(request, *args, **kwargs)