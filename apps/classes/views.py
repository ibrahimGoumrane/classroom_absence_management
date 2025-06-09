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
from apps.users.permissions import IsAdmin, IsTeacherOrAdmin
from apps.students.serializer import StudentSerializer
from rest_framework.permissions import AllowAny
import shutil
from apps.teachers.models import Teacher
from apps.attendance.models import Attendance
from rest_framework.decorators import api_view, permission_classes
from apps.subjects.models import Subject
from apps.subjects.serializer import SubjectReadSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.attendance.serializer import AttendanceReadSerializer

# Create your views here.
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        if self.action == 'get_class_students':
            return [IsAuthenticated(), IsTeacherOrAdmin()]
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
    @action(detail=False, methods=['GET'], url_path='total')
    def get_total_classes(self, request, pk=None):
        """
        Returns the total number of classes in the system.
        """
        total_classes = Class.objects.count()
        return Response({'total': total_classes}, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_class_attendance(request , id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        section_promo = Class.objects.get(id=id)
    except Class.DoesNotExist:
        return Response({"error": "User is not a class"}, status=status.HTTP_403_FORBIDDEN)

    # Get all subjects taught by this class
    subjects = Subject.objects.filter(section_promo=section_promo)

    # Get all attendance records for these subjects
    attendance_records = Attendance.objects.filter(subject__in=subjects)
    
    # You can add filters for specific date ranges, students, etc.
    subject_id = request.query_params.get('subject_id')
    if subject_id:
        attendance_records = attendance_records.filter(subject_id=subject_id)
    
    date_from = request.query_params.get('date_from')
    if date_from:
        attendance_records = attendance_records.filter(date__gte=date_from)
    
    date_to = request.query_params.get('date_to')
    if date_to:
        attendance_records = attendance_records.filter(date__lte=date_to)
    
    serializer = AttendanceReadSerializer(attendance_records, many=True)
    
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_class_subjects(request ,id):
    # Check if the method is GET AND get the id
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        section_promo = Class.objects.get(id=id)
    except Class.DoesNotExist:
        return Response({"error": "User is not a class"}, status=status.HTTP_403_FORBIDDEN)

    # Get all subjects belonging to this class
    subjects = Subject.objects.filter(section_promo=section_promo)
    serializer = SubjectReadSerializer(subjects, many=True)

    return Response(serializer.data)