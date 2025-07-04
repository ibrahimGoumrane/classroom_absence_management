from rest_framework import serializers
from .models import Teacher
from apps.users.serializer import UserLightSerializer, UserSerializer
from apps.users.models import User

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = '__all__'
        extra_kwargs = {'user': {
            'password': {'write_only': True},
        }}  # Hide user in responses
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user_data['role'] = 'teacher'  # Ensure the role is set to 'teacher'
        serializer = UserSerializer(data=user_data)  # Create User instance
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        teacher = Teacher.objects.create(user=user, **validated_data)  # Create Teacher instance
        return teacher

class TeacherReadLightSerializer(serializers.ModelSerializer):
    """Serializer for reading teacher data with minimal fields"""
    user = UserLightSerializer()
    class Meta:
        model = Teacher
        fields = "__all__"