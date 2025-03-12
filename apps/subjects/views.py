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