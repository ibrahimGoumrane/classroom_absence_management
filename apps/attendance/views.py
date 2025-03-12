from django.shortcuts import render
from  rest_framework import viewsets
from .models import Attendance
from .serializer import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from apps.users.permissions import IsTeacher , IsAdmin
# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsTeacher() or IsAdmin()]  # ✅ Fixed instantiation
