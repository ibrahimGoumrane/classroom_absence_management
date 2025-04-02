from rest_framework import viewsets
from .models import Department
from .serializer import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from django.db.models import Count
from rest_framework.response import Response  # <-- Add this import

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view departments
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete

    def get_queryset(self):
        """
        Override the default queryset to annotate each department with the teacher count.
        """
        return Department.objects.annotate(teacher_count=Count('teachers'))

    def list(self, request, *args, **kwargs):
        """
        Overriding list view to include teacher count for each department.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # <-- Return the response with serialized data
