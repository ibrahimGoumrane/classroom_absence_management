from rest_framework import serializers
from .models import User
# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

    def create(self, validated_data):
        """Ensure password is hashed before saving."""
        return User.objects.create_user(**validated_data)  # Uses UserManager's create_user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)