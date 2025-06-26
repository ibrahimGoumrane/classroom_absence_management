from rest_framework import serializers
from .models import Student
from apps.users.serializer import UserSerializer
from apps.studentimages.serializer import StudentImageSerializer


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # Here add also the lastest uploaded image
    latest_image = serializers.SerializerMethodField()
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
    
    def get_latest_image(self, obj):
        """
        Returns the most recently uploaded image for a student
        """
        latest_image = obj.images.order_by('-uploaded_at').first()
        if latest_image:
            return StudentImageSerializer(latest_image).data
        return None
    
class StudentReadLightSerializer(serializers.ModelSerializer):
    """
    Get from the user only the id, firstName , lastName and email
    """
    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'email']