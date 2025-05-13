from rest_framework import serializers
from .models import Attendance
from apps.students.serializer import StudentSerializer
from apps.subjects.serializer import SubjectSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField(read_only=True)
    subject_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Attendance
        fields = "__all__"

    def get_student_details(self, obj):
        return {
            'id': obj.student.id,
            'name': f"{obj.student.user.firstName} {obj.student.user.lastName}"
        }
    
    def get_subject_details(self, obj):
        return {
            'id': obj.subject.id,
            'name': obj.subject.name
        }