from rest_framework import viewsets
from .models import Subject
from .serializer import SubjectReadSerializer, SubjectReadSerializerLight, SubjectWriteSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsTeacherOrAdmin, TeacherObjectOwnerOrAdmin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import datetime
from apps.attendance.models import Attendance
from apps.attendance.serializer import AttendanceReadSerializer, AttendanceReadSerializerLight
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q


# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Custom list method to paginate and filter the results.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results by subject name.
            - teacher_id: Filter by teacher ID.
            - class_id: Filter by class ID.
            - paginated: A boolean to indicate whether to paginate the results (default is True).
        Returns:
             - data: array of Subject objects
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
        teacher_id = request.query_params.get('teacher_id')
        class_id = request.query_params.get('class_id')
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'

        queryset = self.get_queryset()

        if search:
            search_term = search.strip()
            queryset = queryset.filter(Q(name__icontains=search_term))

        if teacher_id:
            queryset = queryset.filter(teacher__id=teacher_id)

        if class_id:
            queryset = queryset.filter(section_promo__id=class_id)

        total_count = queryset.count()

        if paginated:
            start = page * limit
            end = start + limit
            queryset = queryset[start:end]

        serializer = SubjectReadSerializerLight(queryset, many=True)

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

    def get_serializer_class(self):
        """Use different serializers for read/write operations"""
        if self.action in ['create', 'update', 'partial_update']:
            return SubjectWriteSerializer
        return SubjectReadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        # For create require authentication
        elif self.action == 'create':
            return [IsAuthenticated(), IsTeacherOrAdmin()]  # ✅ Fixed instantiation
        # For  update, and delete actions, require either admin or teacher permissions
        return [IsAuthenticated(), TeacherObjectOwnerOrAdmin()]  # ✅ Fixed instantiation

    @action(detail=False, methods=['GET'], url_path='attendance-today')
    def get_classes_attendance_today(self, request):
        """
        Returns attendance records for today, formatted according to the ClassAttendance interface.
        Each record includes the subject details, date, count of present students, and list of absent students.
        """
        today = datetime.date.today()

        # Get all attendance records for today
        attendance_records = Attendance.objects.filter(date__date=today)

        # Call the serializer to format the records
        serializer = AttendanceReadSerializer(attendance_records, many=True)
        # Group by subject
        attendance_by_subject = {}
        for record in serializer.data:
            subject_name = record['subject']['name']
            if subject_name not in attendance_by_subject:
                attendance_by_subject[subject_name] = {
                    'subject': record['subject'],
                    'date': record['date'],
                    'presentStudents': 0,
                    'absentStudents': [],
                }
            if record['status'] == 'present':
                attendance_by_subject[subject_name]['presentStudents'] += 1
            else:
                attendance_by_subject[subject_name]['absentStudents'].append(record['student'])
        results = list(attendance_by_subject.values())
        return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_subjects_attendance_today(request, id):
    """
    Returns attendance records for today for a specific teacher subjects, formatted according to the ClassAttendance interface.
    Each record includes the subject details, date, count of present students, and list of absent students.
    """
    # Check if the method is GET AND get the id
    if request.method != 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    today = datetime.date.today()

    attendance_records = Attendance.objects.filter(date__date=today, subject__teacher__id=id)

    # Call the serializer to format the records
    serializer = AttendanceReadSerializer(attendance_records, many=True)
    # Group by subject
    attendance_by_subject = {}
    for record in serializer.data:
        subject_name = record['subject']['name']
        if subject_name not in attendance_by_subject:
            attendance_by_subject[subject_name] = {
                'subject': record['subject'],
                'date': record['date'],
                'presentStudents': 0,
                'absentStudents': [],
            }
        if record['status'] == 'present':
            attendance_by_subject[subject_name]['presentStudents'] += 1
        else:
            attendance_by_subject[subject_name]['absentStudents'].append(record['student'])
    results = list(attendance_by_subject.values())
    return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subject_attendance(request, id):
    """
    Returns paginated attendance records for a specific subject.
    parameters:
        - page: The page number to retrieve (default is 0)
        - limit: The number of items per page (default is 10)
        - student_id: Filter by student ID (default is None)
        - date_from: Filter by start date (YYYY-MM-DD HH:mm:ss, time is optional)
        - date_to: Filter by end date (YYYY-MM-DD HH:mm:ss, time is optional)
        - status: Filter by attendance status (present/absent)
        - paginated: Boolean to indicate whether to paginate results (default is True)
    Returns:
        - data: array of Attendance objects
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
        subject = Subject.objects.get(id=id)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get pagination parameters
    page = int(request.query_params.get('page', 0))
    limit = int(request.query_params.get('limit', 10))
    paginated = request.query_params.get('paginated', 'true').lower() == 'true'

    # Build base queryset
    attendance = Attendance.objects.filter(subject=subject)

    # Apply filters
    student_id = request.query_params.get('student_id')
    if student_id:
        attendance = attendance.filter(student_id=student_id)

    date_from = request.query_params.get('date_from')
    if date_from:
        attendance = attendance.filter(date__gte=date_from)

    date_to = request.query_params.get('date_to')
    if date_to:
        attendance = attendance.filter(date__lte=date_to)

    status_filter = request.query_params.get('status')
    if status_filter:
        attendance = attendance.filter(status__iexact=status_filter)

    # Get total count before pagination
    total_count = attendance.count()

    # Apply pagination
    if paginated:
        start = page * limit
        end = start + limit
        attendance = attendance[start:end]

    serializer = AttendanceReadSerializerLight(attendance, many=True)

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
