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

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'departments_with_teacher_count']:  # Allow anyone to view departments
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    def get_queryset(self):
        """
        Override the default queryset to annotate each department with the teacher count.
        """
        return Department.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Default list view for departments, without teacher count.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='with-teacher-count')
    def departments_with_teacher_count(self, request, *args, **kwargs):
        """
        Custom endpoint that includes teacher count for each department.
        """
        queryset = Department.objects.annotate(teacherCount=Count('teachers'))
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
