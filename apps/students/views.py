from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework import status
from .models import Student
from .serializer import StudentSerializer
import os
from django.conf import settings
from apps.users.serializer import UserSerializer
from apps.classes.models import Class
from apps.users.permissions import IsAdmin
from apps.users.models import User
from apps.classes.models import Class
from rest_framework import serializers
import shutil
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.attendance.serializer import AttendanceReadSerializer
# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view students
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    # This method is overridden to create a folder with the user ID inside the section_promo directory and create a user then create a student
    def create(self, request, *args, **kwargs):
        # Create user
        Student_serializer = StudentSerializer(data=request.data)
        Student_serializer.is_valid(raise_exception=True)
        student = Student_serializer.save()
        
        # Get section_promo (class name) from request data
        class_id = student.section_promo.id
        if not class_id:
            return Response({"error": "section_promo (class ID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create folder with user ID inside the section_promo directory
        folder_path = os.path.join(settings.MEDIA_ROOT, class_instance.name, str(student.id))
        os.makedirs(folder_path, exist_ok=True)
        
        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
    
    # We will override the update method to update te user then the student
    def update(self, request, *args, **kwargs):
        # Extract user data from request
        user_data = request.data.pop('user')
        student_instance = self.get_object()

        if user_data:
            user = student_instance.user
            new_email = user_data.get('email', user.email)  # Default to current email

            # ✅ Check if email is actually changing before validation
            if new_email != user.email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
                raise serializers.ValidationError({"user": {"email": ["This email is already taken by another user."]}})

            # Update user data
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # ✅ Now validate and update the student instance
        student_serializer = self.get_serializer(student_instance, data=request.data, partial=True)
        student_serializer.is_valid(raise_exception=True)
        student = student_serializer.save()

        return Response(StudentSerializer(student).data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        student = self.get_object()  # Get student instance
        user = student.user  # Get associated user
        class_instance = student.section_promo  # Get section_promo (class)

        # ✅ Construct folder path
        folder_path = os.path.join(settings.MEDIA_ROOT, class_instance.name, str(student.id))

        # ✅ Delete student record
        student.delete()

        # ✅ Delete user account
        user.delete()

        # ✅ Remove the student's folder if it exists
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Recursively delete folder

        return Response({"message": "Student and associated user deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_attendance(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    attendances = student.attendance_records.all()
    
    # Add filters based on query parameters
    subject_id = request.query_params.get('subject_id')
    if subject_id:
        attendances = attendances.filter(subject_id=subject_id)
    
    date_from = request.query_params.get('date_from')
    if date_from:
        attendances = attendances.filter(date__gte=date_from)
    
    date_to = request.query_params.get('date_to')
    if date_to:
        attendances = attendances.filter(date__lte=date_to)
    
    status_param = request.query_params.get('status')
    if status_param:
        attendances = attendances.filter(status=status_param)
    
    attendances_data = AttendanceReadSerializer(attendances, many=True).data
    return Response(attendances_data, status=status.HTTP_200_OK)