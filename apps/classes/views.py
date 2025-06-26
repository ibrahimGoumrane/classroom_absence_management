from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Class
from .serializer import ClassSerializer
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from apps.users.permissions import IsAdmin, IsTeacherOrAdmin
from apps.students.serializer import StudentReadLightSerializer
from rest_framework.permissions import AllowAny
import shutil
from apps.attendance.models import Attendance
from rest_framework.decorators import api_view, permission_classes
from apps.subjects.models import Subject
from apps.subjects.serializer import SubjectReadSerializerLight
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.attendance.serializer import AttendanceReadSerializerLight
from django.db.models import Q


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        if self.action == 'get_class_students':
            return [IsAuthenticated(), IsTeacherOrAdmin()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    def list(self, request, *args, **kwargs):
        """
        Custom list method to paginate the results.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results by class name (default is an empty string).
            - paginated: A boolean to indicate whether to paginate the results (default is True).
        Returns:
             - data: array of Department objects
             - metadata: {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
             }
        """
        page = int(request.query_params.get('page', 0))
        limit = int(request.query_params.get('limit', 10))
        search = request.query_params.get('search', '')
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'

        queryset = self.get_queryset()

        if search:
            search_term = search.strip()
            queryset = queryset.filter(Q(name__icontains=search_term))

        total_count = queryset.count()

        if paginated:
            start = page * limit
            end = start + limit
            queryset = queryset[start:end]

        serializer = ClassSerializer(queryset, many=True)

        return Response(
            {
                'data': serializer.data,
                'metadata': {
                    'page': page if paginated else 0,
                    'limit': limit if paginated else total_count,
                    'total': total_count,
                    'totalPages': (total_count + limit - 1) // limit if paginated else 1,
                },
            },
            status=status.HTTP_200_OK,
        )

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

        # Here instead of creating new folder, we will update the folder name
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
        Returns the paginated list of students belonging to the given class.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results (default is an empty string).
            - paginated: A boolean to indicate whether to paginate the results (default is True).
        Returns:
             - data: array of Student objects
             - metadata: {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
             }
        """
        try:
            cls = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=404)

        page = int(request.query_params.get('page', 0))
        limit = int(request.query_params.get('limit', 10))
        search = request.query_params.get('search', '')
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'

        students = cls.students.all()

        if search:
            search_term = search.strip()
            students = students.filter(
                Q(user__firstName__icontains=search_term)
                | Q(user__lastName__icontains=search_term)
                | Q(user__email__icontains=search_term)
            )

        total_count = students.count()

        if paginated:
            start = page * limit
            end = start + limit
            students = students[start:end]

        serializer = StudentReadLightSerializer(students, many=True)

        return Response(
            {
                'data': serializer.data,
                'metadata': {
                    'page': page if paginated else 0,
                    'limit': limit if paginated else total_count,
                    'total': total_count,
                    'totalPages': (total_count + limit - 1) // limit if paginated else 1,
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['GET'], url_path='total')
    def get_total_classes(self, request, pk=None):
        """
        Returns the total number of classes in the system.
        """
        total_classes = Class.objects.count()
        return Response({'total': total_classes}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_class_attendance(request, id):
    """
    Returns the paginated list of attendance records for a class.
    parameters:
        - page: The page number to retrieve (default is 0)
        - limit: The number of items per page (default is 10)
        - student_id: Filter by student ID (default is None)
        - subject_id: Filter by subject ID (default is None)
        - date_from: Filter by start date (YYYY-MM-DD HH:mm:ss, time is optional)
        - date_to: Filter by end date (YYYY-MM-DD HH:mm:ss, time is optional)
        - status: Filter by attendance status (present/absent)
        - paginated: Boolean to indicate whether to paginate results (default is True)
    """
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        section_promo = Class.objects.get(id=id)
    except Class.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_403_FORBIDDEN)

    # Get pagination parameters
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    # Get all subjects taught by this class
    subjects = Subject.objects.filter(section_promo=section_promo)

    # Get all attendance records for these subjects
    attendance_records = Attendance.objects.filter(subject__in=subjects)

    # Apply filters
    filters = Q()

    student_id = request.query_params.get('student_id')
    if student_id:
        filters &= Q(student__id=student_id)

    subject_id = request.query_params.get('subject_id')
    if subject_id:
        filters &= Q(subject__id=subject_id)

    date_from = request.query_params.get('date_from')
    if date_from:
        filters &= Q(date__gte=date_from)

    date_to = request.query_params.get('date_to')
    if date_to:
        filters &= Q(date__lte=date_to)

    status_filter = request.query_params.get('status')
    if status_filter:
        filters &= Q(status__iexact=status_filter)

    # Apply filters to queryset
    attendance_records = attendance_records.filter(filters)

    # Get total count before pagination
    total_count = attendance_records.count()

    # Apply pagination
    if paginated:
        start = page * limit
        end = start + limit
        attendance_records = attendance_records[start:end]

    serializer = AttendanceReadSerializerLight(attendance_records, many=True)

    return Response(
        {
            'data': serializer.data,
            'metadata': {
                'page': page if paginated else 0,
                'limit': limit if paginated else total_count,
                'total': total_count,
                'totalPages': (total_count + limit - 1) // limit if paginated else 1,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_class_subjects(request, id):
    """
    Returns the paginated list of subjects for a class.
    parameters:
        - page: The page number to retrieve (default is 0)
        - limit: The number of items per page (default is 10)
        - search: Search term to filter by subject name
        - teacher_id: Filter by teacher ID
        - paginated: Boolean to indicate whether to paginate results (default is True)
    Returns:
        - data: array of Subject objects
        - metadata: {
            - page: number,
            - limit: number,
            - total: number,
            - totalPages: number
        }
    """
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        section_promo = Class.objects.get(id=id)
    except Class.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_403_FORBIDDEN)

    # Get pagination parameters
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')
    teacher_id = request.query_params.get('teacher_id')
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    # Get all subjects belonging to this class
    subjects = Subject.objects.filter(section_promo=section_promo)

    # Apply filters
    if search:
        search_term = search.strip()
        subjects = subjects.filter(Q(name__icontains=search_term))

    if teacher_id:
        subjects = subjects.filter(teacher__id=teacher_id)

    # Get total count before pagination
    total_count = subjects.count()

    # Apply pagination
    if paginated:
        start = page * limit
        end = start + limit
        subjects = subjects[start:end]

    serializer = SubjectReadSerializerLight(subjects, many=True)

    return Response(
        {
            'data': serializer.data,
            'metadata': {
                'page': page if paginated else 0,
                'limit': limit if paginated else total_count,
                'total': total_count,
                'totalPages': (total_count + limit - 1) // limit if paginated else 1,
            },
        },
        status=status.HTTP_200_OK,
    )
