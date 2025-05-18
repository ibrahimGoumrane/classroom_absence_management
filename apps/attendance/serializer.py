from rest_framework import serializers

from apps.students.models import Student
from .models import Attendance
from apps.students.serializer import StudentSerializer
from apps.subjects.serializer import SubjectReadSerializer
from apps.subjects.models import Subject

class AttendanceReadSerializer(serializers.ModelSerializer):
    """Serializer for reading attendance - includes nested objects"""
    student = StudentSerializer()
    subject = SubjectReadSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating attendance - accepts IDs"""
    student_id = serializers.PrimaryKeyRelatedField(
        source='student',
        queryset=Student.objects.all(),
        required=False,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source='subject',
        queryset=Subject.objects.all(),
                required=False,

    )

    class Meta:
        model = Attendance
        fields = ['id', 'student_id', 'subject_id', 'date', 'status']        

