from rest_framework import serializers
from .models import Student, StudentImage
from apps.users.serializer import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {'user': {
            'password': {'write_only': True},
        }}
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user_data['role'] = 'student'  # Ensure the role is set to 'teacher'
        serializer = UserSerializer(data=user_data)  # Create User instance
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        teacher = Student.objects.create(user=user, **validated_data)  # Create Teacher instance
        return teacher
    
class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = '__all__'

 
        