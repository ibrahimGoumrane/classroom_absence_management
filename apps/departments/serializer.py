from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    teacher_count = serializers.IntegerField(read_only=True)  # Add this line to include teacher count in the output

    class Meta:
        model = Department
        fields = ['id', 'name', 'teacher_count']  # Include teacher_count in the fields
