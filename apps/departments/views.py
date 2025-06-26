from rest_framework import viewsets
from .models import Department
from .serializer import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin, IsTeacherOrAdmin
from rest_framework.permissions import AllowAny
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.teachers.serializer import TeacherReadLightSerializer
from rest_framework import status as Status


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view departments
            return [AllowAny()]
        if self.action in ['get_teachers_for_department']:
            return [IsAuthenticated(), IsTeacherOrAdmin()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    def list(self, request, *args, **kwargs):
        """
        Custom list method to paginate the results.
        parameters:
            - page: The page number to retrieve (default is 0).
            - limit: The number of items per page (default is 10).
            - search: A search term to filter the results by department name or desc (default is an empty string).
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
            queryset = queryset.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))

        total_count = queryset.count()

        if paginated:
            start = page * limit
            end = start + limit
            queryset = queryset[start:end]

        serializer = DepartmentSerializer(queryset, many=True)

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
            status=Status.HTTP_200_OK,
        )

    @action(detail=True, methods=['get'], url_path='teachers')
    def get_teachers_for_department(self, request, pk=None):
        """
        Returns the paginated list of teachers belonging to the given department.
        parameters:
            - page: The page number to retrieve (default is 0)
            - limit: The number of items per page (default is 10)
            - search: Search term to filter by name or email
            - paginated: Boolean to indicate whether to paginate results (default is True)
        Returns:
            - data: array of Teacher objects
            - metadata: {
                - page: number,
                - limit: number,
                - total: number,
                - totalPages: number
            }
        """
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found.'}, status=404)

        # Get pagination parameters
        page = int(request.query_params.get('page', 0))
        limit = int(request.query_params.get('limit', 10))
        search = request.query_params.get('search', '')
        paginated = request.query_params.get('paginated', 'true').lower() == 'true'

        teachers = department.teachers.all()

        if search:
            search_term = search.strip()
            teachers = teachers.filter(
                Q(user__firstName__icontains=search_term)
                | Q(user__lastName__icontains=search_term)
                | Q(user__email__icontains=search_term)
            )

        total_count = teachers.count()

        if paginated:
            start = page * limit
            end = start + limit
            teachers = teachers[start:end]

        serializer = TeacherReadLightSerializer(teachers, many=True)

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
            status=Status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'], url_path='attendance-total')
    def get_departments_attendance(self, request):
        """
        Returns the attendance count for each department.
        """
        departments_data = Department.objects.annotate(
            total=Count('teachers__subjects__attendance_records')
        ).values(
            'name', 'total'
        )  # Only select 'name' and 'total' as 'id' is not needed in final output

        # Transform the QuerySet into the desired JSON format
        formatted_data = []
        for department in departments_data:
            formatted_data.append(
                {
                    "department": department['name'],  # Map 'name' to 'department'
                    "attendance": department['total'] * 100,  # Map 'total' to 'attendance'
                }
            )

        return Response(formatted_data, status=Status.HTTP_200_OK)
