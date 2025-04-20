from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Class
from .serializer import ClassSerializer
import os
from django.conf import settings
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from apps.users.permissions import IsAdmin
from apps.students.serializer import StudentSerializer
from apps.studentimages.serializer import StudentImageSerializer
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
    
    @action(detail=False, methods=['get'], url_path='with-student-count')
    def classes_with_student_counts(self, request, *args, **kwargs):
        """
        Custom endpoint that includes student count for each department.
        """
        queryset = Class.objects.annotate(studentCount=Count('students'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='with-student-count')
    def class_with_student_count(self, request, pk=None):
        """
        Returns the specified class with its student count.
        """
        try:
            cls = Class.objects.annotate(studentCount=Count('students')).get(pk=pk)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        serializer = self.get_serializer(cls)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='students')
    def get_class_students(self, request, pk=None):
        """
        Returns the list of students belonging to the given class.
        """
        try:
            cls = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        students = cls.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)