from rest_framework import viewsets
from .models import Department
from .serializer import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action

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
