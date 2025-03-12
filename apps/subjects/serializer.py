from rest_framework import serializers
from .models import Subject
from apps.teachers.serializer import TeacherSerializer

class SubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'name' ,'teacher']