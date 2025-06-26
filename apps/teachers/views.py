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
from apps.subjects.serializer import  SubjectReadSerializerWithoutTeacher
from apps.attendance.models import Attendance
from apps.attendance.serializer import AttendanceReadSerializer, AttendanceReadSerializerLight
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q


# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    # I want to customize the default list method to Paginate the results using the following params
    def list(self, request, *args, **kwargs):
        '''
        Custom list method to paginate the results.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results (default is an empty string).
            - paginated: A boolean to indicate whether to paginate the results (default is True).
            - department: The department to filter the results (default is an empty string).
        Returns:
             - data: array of Teacher objects
             - metadata: {
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
        department = request.query_params.get('department', '')

        queryset = self.get_queryset()
        
        # Apply filters
        if department:
            queryset = queryset.filter(department__id=department)
        
        if search:
            search_term = search.strip()  # Remove leading/trailing whitespace
            queryset = queryset.filter(
                Q(user__firstName__icontains=search_term) | 
                Q(user__lastName__icontains=search_term) | 
                Q(user__email__icontains=search_term)
            )
        
        # ✅ Get the total count AFTER applying filters
        total_count = queryset.count()
        
        # Apply pagination
        if paginated:
            start = page * limit
            end = start + limit
            queryset = queryset[start:end]
        serializer = TeacherSerializer(queryset, many=True)
        
        return Response({
            'data': serializer.data,
            'metadata': {
                'page': page if paginated else 0,  # If paginated is false, page should be 0
                'limit': limit if paginated else total_count,  # If paginated is false, limit should be total count
                'total': total_count,  # ✅ Use filtered count
                'totalPages': (total_count + limit - 1) // limit if paginated else 1,  # Calculate total pages
                'department': department if department else None
            }
        }, status=status.HTTP_200_OK)

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

# Add some pagination to the subjects of a teacher
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_subjects(request ,id):
    """
    Returns all subjects taught by a teacher.
    Parameters:
        - id: The ID of the teacher.
    Query Parameters:
        - page: The page number to retrieve (default is 0).
        - limit: The number of items per page (default is 10).
        - search: A search term to filter the results (default is an empty string).
        - paginated: A boolean to indicate whether to paginate the results (default is True).
    Returns:
       A paginated list of subjects taught by the teacher.
       - data: array of Subject objects
         - metadata: {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
          }
       """
    # Check if the teacher exists
    try:
        Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    

    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'
    queryset = Subject.objects.filter(teacher__id=id)

    if search:
        queryset = queryset.filter(name__icontains=search)

    total_count = queryset.count()
    if paginated:
        start = page * limit
        end = start + limit
        queryset = queryset[start:end]
    else:
        start = 0
        end = total_count
    # Here
    serializer = SubjectReadSerializerWithoutTeacher(queryset, many=True)
    return Response({
        "data": serializer.data,
        "metadata": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "totalPages": (total_count + limit - 1) // limit
        }
    })


# Get all attendance records for a teacher paginated 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_attendance(request , id):
    """
    Returns all attendance records for a teacher.
    Parameters:
        - id: The ID of the teacher.
    Query Parameters:
        - subject_id: Filter by specific subject ID (optional).
        - date_from: Filter records from this date (optional).
        - student_id: Filter by specific student ID (optional).
        - date_to: Filter records to this date (optional).
        - page: The page number to retrieve (default is 0).
        - limit: The number of items per page (default is 10).
        - paginated: A boolean to indicate whether to paginate the results (default is True).
    Returns:
        A paginated list of attendance records for the teacher.
        - data: array of Attendance objects
        - metadata: {
            - page: number,
            - limit: number,
            - total: number,
            - totalPages: number
        }
    """
        # Check if the method is GET AND get the id 
    if request.method != 'GET':
         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    # Check if the teacher exists
    try:
        Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "User is not a teacher"}, status=status.HTTP_403_FORBIDDEN)
    
    queryset = Attendance.objects.filter(subject__teacher__id=id).order_by('-date')  # Get all attendance records for the teacher
    # Apply filters based on query parameters
    student_id = request.query_params.get('student_id')
    if student_id:
        queryset = queryset.filter(student__id=student_id)

    subject_id = request.query_params.get('subject_id')
    if subject_id:
        queryset = queryset.filter(subject__id=subject_id)  

    # Get attendance records within a date range
    date_from = request.query_params.get('date_from')
    if date_from:
        queryset = queryset.filter(date__gte=date_from)

    date_to = request.query_params.get('date_to')
    if date_to:
        queryset = queryset.filter(date__lte=date_to)

    # Get total count after applying filters
    total_count = queryset.count()
    if paginated:
        start = page * limit
        end = start + limit
        queryset = queryset[start:end]
    else:
        start = 0
        end = total_count

    # Serialize the attendance records
    serializer = AttendanceReadSerializerLight(queryset, many=True)
    return Response({
        "data": serializer.data,
        "metadata": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "totalPages": (total_count + limit - 1) // limit
        }
    })

