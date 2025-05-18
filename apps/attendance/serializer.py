from rest_framework import serializers
from .models import Attendance
from apps.students.serializer import StudentSerializer
from apps.subjects.serializer import SubjectReadSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectReadSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'

