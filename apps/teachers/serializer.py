from rest_framework import serializers
from .models import Teacher
from apps.users.serializer import UserSerializer
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
        user = User.objects.create(**user_data)  # Create User instance
        teacher = Teacher.objects.create(user=user, **validated_data)  # Create Teacher instance
        return teacher
    
