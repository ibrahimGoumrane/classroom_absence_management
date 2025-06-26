from rest_framework import serializers
from .models import Subject
from apps.teachers.models import Teacher
from apps.teachers.serializer import TeacherReadLightSerializer, TeacherSerializer
from apps.classes.models import Class
from apps.classes.serializer import ClassSerializer


class SubjectReadSerializer(serializers.ModelSerializer):
    """Serializer for reading subjects - includes nested objects"""
    teacher = TeacherSerializer()
    section_promo = ClassSerializer()
    
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectReadSerializerLight(serializers.ModelSerializer):
    """
    Serializer for reading subjects 
    """
    teacher = TeacherReadLightSerializer()
    section_promo = ClassSerializer()
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating subjects - accepts IDs"""
    teacher_id = serializers.PrimaryKeyRelatedField(
        source='teacher',
        queryset=Teacher.objects.all(),
    )
    section_promo_id = serializers.PrimaryKeyRelatedField(
        source='section_promo',
        queryset=Class.objects.all(),
    )
    
    class Meta:
        model = Subject
        fields = ['id', 'name',  'teacher_id', 'section_promo_id']