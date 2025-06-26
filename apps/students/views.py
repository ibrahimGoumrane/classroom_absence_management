from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework import status
from django.db.models import Q

from apps.subjects.models import Subject
from apps.subjects.serializer import SubjectReadSerializer, SubjectReadSerializerLight
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
from apps.attendance.serializer import AttendanceReadSerializer, AttendanceReadSerializerLight
from rest_framework.decorators import action
# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view students
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete
    # We wil override the default list method to filter students by class and add pagination 
    def list(self, request, *args, **kwargs):
        '''
        List all students or filter by class ID.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results (default is an empty string).
            - paginated: A boolean to indicate whether to paginate the results (default is True).
            - class: The class to filter the results (default is an empty string).
        returns:
            - data: A list of students or a paginated response if paginated is True.
            - metadata : {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
            }
        '''
        
        page = int(request.query_params.get('page', 0))
        limit = int(request.query_params.get('limit', 10))
        search = request.query_params.get('search', '')
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'
        class_id = request.query_params.get('class', '')

        queryset = self.get_queryset()
        
        # Apply filters
        if class_id:
            queryset = queryset.filter(section_promo__id=class_id)
        
        if search:
            search_term = search.strip()  # Remove leading/trailing whitespace
            queryset = queryset.filter(
                Q(user__firstName__icontains=search_term) | 
                Q(user__lastName__icontains=search_term) | 
                Q(user__email__icontains=search_term)
            )
        
        # Get the total count AFTER applying filters
        total_count = queryset.count()
        
        # Apply pagination
        if paginated:
            start = page * limit
            end = start + limit
            queryset = queryset[start:end]
        
        serializer = StudentSerializer(queryset, many=True)
        
        return Response({
            'data': serializer.data,
            'metadata': {
                'page': page,
                'limit': limit,
                'total': total_count,  # Use filtered count
                'totalPages': (total_count + limit - 1) // limit,  # Calculate based on filtered count
                'class': class_id if class_id else None
            }
        }, status=status.HTTP_200_OK)


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
    @action(detail=False, methods=['GET'], url_path='total')
    def get_total_students(self, request):
        """
        Returns the total number of students in the system.
        """
        total_students = Student.objects.count()
        return Response({"total": total_students}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_attendance(request, id):
    """
    Returns all attendance records for a student.
    Parameters:
        - id: The ID of the student.
    Query Parameters:
        - subject_id: Filter by specific subject ID (optional).
        - date_from: Filter records from this date (optional).
        - date_to: Filter records to this date (optional).
        - status: Filter by attendance status (optional).
        - page: The page number to retrieve (default is 0).
        - limit: The number of items per page (default is 10).
        - paginated: A boolean to indicate whether to paginate the results (default is True).
    Returns:
        A paginated list of attendance records for the student.
        - data: array of Attendance objects
        - metadata: {
            - page: number,
            - limit: number,
            - total: number,
            - totalPages: number
        }
    """
    # Get pagination parameters
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    attendances = student.attendance_records.all().order_by('-date')  # Get all attendance records for the student
    
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
    
    # Get total count after applying filters
    total_count = attendances.count()
    
    if paginated:
        start = page * limit
        end = start + limit
        attendances = attendances[start:end]
    
    serializer = AttendanceReadSerializerLight(attendances, many=True)
    return Response({
        "data": serializer.data,
        "metadata": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "totalPages": (total_count + limit - 1) // limit
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_subjects(request, id):
    """
    Returns all subjects for a student's class.
    Parameters:
        - id: The ID of the student.
    Query Parameters:
        - page: The page number to retrieve (default is 0).
        - limit: The number of items per page (default is 10).
        - search: A search term to filter the results (default is an empty string).
        - paginated: A boolean to indicate whether to paginate the results (default is True).
    Returns:
       A paginated list of subjects for the student's class.
       - data: array of Subject objects
         - metadata: {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
          }
       """
    # Get pagination parameters
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    
    queryset = Subject.objects.filter(section_promo=student.section_promo)

    if search:
        queryset = queryset.filter(name__icontains=search)

    total_count = queryset.count()
    
    if paginated:
        start = page * limit
        end = start + limit
        queryset = queryset[start:end]

    serializer = SubjectReadSerializerLight(queryset, many=True)
    
    return Response({
        "data": serializer.data,
        "metadata": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "totalPages": (total_count + limit - 1) // limit
        }
    }, status=status.HTTP_200_OK)