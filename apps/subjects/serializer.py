from rest_framework import serializers
from .models import Subject
from apps.teachers.models import Teacher
from apps.teachers.serializer import TeacherSerializer
from apps.classes.models import Class
from apps.classes.serializer import ClassSerializer


class SubjectReadSerializer(serializers.ModelSerializer):
    """Serializer for reading subjects - includes nested objects"""
    teacher = TeacherSerializer()
    section_promo = ClassSerializer()
    
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectReadSerializerWithoutTeacher(serializers.ModelSerializer):
    """Serializer for reading subjects without teacher details"""
    section_promo = ClassSerializer()
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'section_promo']
class SubjectReadSerializerLight(serializers.ModelSerializer):
    """
    Serializer for reading subjects 
    """
    class Meta:
        model = Subject
        fields = ['id', 'name']

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