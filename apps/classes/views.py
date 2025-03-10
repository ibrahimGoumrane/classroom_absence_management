from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Class
from .serializer import ClassSerializer
import os
from django.conf import settings

# Create your views here.
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    # Default create method is overridden to create a folder with the class name
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        class_name = response.data.get('name')
        folder_path = os.path.join(settings.MEDIA_ROOT, class_name)
        os.makedirs(folder_path, exist_ok=True)
        return response

    # Default update method is overridden to update the folder name plus the class name
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        class_name = response.data.get('name')
        
        #Here instead of creating new folder, we will update the folder name
        old_class_name = Class.objects.get(id=kwargs['pk']).name
        old_folder_path = os.path.join(settings.MEDIA_ROOT, old_class_name)
        new_folder_path = os.path.join(settings.MEDIA_ROOT, class_name)
        os.rename(old_folder_path, new_folder_path)
        return response