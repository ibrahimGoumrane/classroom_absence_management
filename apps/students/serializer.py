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

class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = '__all__'

 
        