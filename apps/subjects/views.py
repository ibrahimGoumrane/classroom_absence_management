from django.shortcuts import render
from rest_framework import viewsets
from .models import Subject
from .serializer import SubjectSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsTeacher , IsAdmin
from rest_framework.permissions import AllowAny
# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsTeacher() or IsAdmin()]  # Require admin permissions for create, update, and delete


    def perform_create(self, serializer):
        # Set the teacher to the currently authenticated user
        serializer.save(teacher=self.request.user.teacher_profile)

    def perform_update(self, serializer):
        # Ensure the teacher cannot be changed
        serializer.save(teacher=self.request.user.teacher_profile)