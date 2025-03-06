from rest_framework import serializers
from .models import Attendance
from apps.students.serializer import StudentSerializer
from apps.subjects.serializer import SubjectSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()
    class Meta:
        model = Attendance
        fields = '__all__'