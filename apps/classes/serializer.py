from rest_framework import serializers
from .models import Class
from django.db.models import Count

class ClassSerializer(serializers.ModelSerializer):
    studentCount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Class
        fields = ['id', 'name', 'studentCount']
    def get_studentCount(self, obj):
        # If studentCount is already annotated from the queryset
        if hasattr(obj, 'studentCount'):
            return obj.studentCount
            
        # Otherwise, calculate it on-demand
        return obj.students.count() if hasattr(obj, 'students') else 0