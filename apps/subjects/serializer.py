from rest_framework import serializers
from .models import Subject
from apps.teachers.serializer import TeacherSerializer
from apps.classes.serializer import ClassSerializer

class SubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    section_promo = ClassSerializer(read_only=True)
    class Meta:
        model = Subject
        fields = "__all__"
        