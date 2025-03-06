from rest_framework import serializers
from .models import Subject
from apps.teachers.serializer import TeacherSerializer

class SubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    class Meta:
        model = Subject
        fields = '__all__'