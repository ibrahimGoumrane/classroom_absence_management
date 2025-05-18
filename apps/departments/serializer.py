from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    teacherCount = serializers.SerializerMethodField(read_only=True) # Add this line to include teacher count in the output
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'teacherCount']  # Include teacher_count in the fields
    def get_teacherCount(self, obj):
        # If teacherCount is already annotated from the queryset
        if hasattr(obj, 'teacherCount'):
            return obj.teacherCount
            
        # Otherwise, calculate it on-demand
        return obj.teachers.count() if hasattr(obj, 'teachers') else 0