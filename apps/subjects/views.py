from django.shortcuts import render
from rest_framework import viewsets

from .models import Subject
from .serializer import SubjectReadSerializer ,SubjectWriteSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsTeacherOrAdmin, TeacherObjectOwnerOrAdmin
from rest_framework.permissions import AllowAny

# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
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
            return [IsAuthenticated() , IsTeacherOrAdmin()]  # ✅ Fixed instantiation
        # For  update, and delete actions, require either admin or teacher permissions
        return [IsAuthenticated(), TeacherObjectOwnerOrAdmin()]  # ✅ Fixed instantiation