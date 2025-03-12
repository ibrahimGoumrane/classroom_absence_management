from django.shortcuts import render
from rest_framework import viewsets
from .models import Subject
from .serializer import SubjectSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsTeacher
# Create your views here.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        # Set the teacher to the currently authenticated user
        serializer.save(teacher=self.request.user.teacher_profile)

    def perform_update(self, serializer):
        # Ensure the teacher cannot be changed
        serializer.save(teacher=self.request.user.teacher_profile)