from django.shortcuts import render
from rest_framework import viewsets

from apps.students.models import Student
from .models import Teacher
from .serializer import TeacherSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from apps.users.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializer import UserSerializer
from apps.users.models import User
from rest_framework import serializers
from apps.subjects.models import Subject
from apps.subjects.serializer import SubjectReadSerializer
from apps.attendance.models import Attendance
from apps.attendance.serializer import AttendanceReadSerializer
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete


    def create(self, request, *args, **kwargs):
        teacher_serializer = self.get_serializer(data=request.data)  # Now it accepts full `user` data
        teacher_serializer.is_valid(raise_exception=True)
        teacher = teacher_serializer.save()

        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        teacher_instance = self.get_object()

        user_data = request.data.pop('user', None)  # Extract user data safely

        if user_data:
            user = teacher_instance.user
            new_email = user_data.get('email', user.email)  # Default to current email

            # ✅ Check if email is actually changing before validation
            if new_email != user.email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
                raise serializers.ValidationError({"user": {"email": ["This email is already taken by another user."]}})

            # Update user data
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # ✅ Now validate and update the teacher instance
        teacher_serializer = self.get_serializer(teacher_instance, data=request.data, partial=True)
        teacher_serializer.is_valid(raise_exception=True)
        teacher = teacher_serializer.save()

        return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        teacher_instance = self.get_object()
        user = teacher_instance.user  # Get the associated user

        self.perform_destroy(teacher_instance)  # Delete teacher
        user.delete()  # Delete the associated user

        return Response({"message": "Teacher deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_subjects(request ,id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    # Get all subjects taught by this teacher
    subjects = Subject.objects.filter(teacher=teacher)
    serializer = SubjectReadSerializer(subjects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_attendance(request , id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    # Get all subjects taught by this teacher
    subjects = Subject.objects.filter(teacher=teacher)
    
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
def get_teacher_total_subjects(request ,id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    total_subjects = Subject.objects.filter(teacher=teacher).count()

    return Response({"total": total_subjects}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_total_students(request ,id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    subjects = Subject.objects.filter(teacher=teacher)
    total_students = Student.objects.filter(section_promo__in=set(subject.section_promo for subject in subjects)).count()
    
    return Response({"total": total_students}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_total_classes(request ,id):
    # Check if the method is GET AND get the id 
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    subjects = Subject.objects.filter(teacher=teacher)
    total_classes = len(set(subject.section_promo for subject in subjects))
    
    return Response({"total": total_classes}, status=status.HTTP_200_OK)