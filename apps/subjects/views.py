from django.shortcuts import render
from rest_framework import viewsets

from .models import Subject
from .serializer import SubjectReadSerializer ,SubjectWriteSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsTeacherOrAdmin, TeacherObjectOwnerOrAdmin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import datetime
from apps.attendance.models import Attendance
from apps.attendance.serializer import AttendanceReadSerializer

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
    
    @action(detail=False, methods=['GET'], url_path='attendance-today')
    def get_classes_attendance_today(self, request):
        """
        Returns attendance records for today, formatted according to the ClassAttendance interface.
        Each record includes the subject details, date, count of present students, and list of absent students.
        """
        today = datetime.date.today()
        
        # Get all attendance records for today
        attendance_records = Attendance.objects.filter(date__date=today)
        
        # Call the serializer to format the records
        serializer = AttendanceReadSerializer(attendance_records, many=True)
        # Group by subject 
        attendance_by_subject = {}
        for record in serializer.data:
            subject_name = record['subject']['name']
            if subject_name not in attendance_by_subject:
                attendance_by_subject[subject_name] = {
                    'subject': record['subject'],
                    'date': record['date'],
                    'presentStudents': 0,
                    'absentStudents': []
                }
            if record['status'] == 'present':
                attendance_by_subject[subject_name]['presentStudents'] += 1
            else:
                attendance_by_subject[subject_name]['absentStudents'].append(record['student'])
        results = list(attendance_by_subject.values())
        return Response(results, status=status.HTTP_200_OK)
