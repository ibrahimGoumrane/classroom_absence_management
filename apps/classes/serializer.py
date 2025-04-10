from rest_framework import serializers
from .models import Class

class ClassSerializer(serializers.ModelSerializer):
    studentCount = serializers.IntegerField(read_only=True)
    class Meta:
        model = Class
        fields = ['id', 'name', 'studentCount']