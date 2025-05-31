from rest_framework import viewsets
from .models import Department
from .serializer import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.teachers.serializer import TeacherSerializer
from rest_framework import status as Status

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view departments
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    def list(self, request, *args, **kwargs):
        """
        Default list view for departments, without teacher count.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='teachers')
    def get_teachers_for_department(self, request, pk=None):
        """
        Returns the list of teachers belonging to the given department.
        """
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({'detail': 'Department not found.'}, status=404)

        teachers = department.teachers.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path='attendance-total')
    def get_departments_attendance(self, request):
        """
        Returns the attendance count for each department.
        """
        departments_data = Department.objects.annotate(
            total=Count('teachers__subjects__attendance_records')
        ).values('name', 'total') # Only select 'name' and 'total' as 'id' is not needed in final output

        # Transform the QuerySet into the desired JSON format
        formatted_data = []
        for department in departments_data:
            formatted_data.append({
                "department": department['name'],   # Map 'name' to 'department'
                "attendance": department['total'] * 100   # Map 'total' to 'attendance'
            })

        return Response(formatted_data, status=Status.HTTP_200_OK)
