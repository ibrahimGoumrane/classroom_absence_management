from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from .models import User
from .serializer import UserSerializer, LoginSerializer
from .permissions import IsAdminOrOwner
from apps.students.serializer import StudentSerializer
from apps.classes.models import Class
from django.conf import settings
import os



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated , IsAdminOrOwner]

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Create user
        Student_serializer = StudentSerializer(data=request.data)
        Student_serializer.is_valid(raise_exception=True)
        student = Student_serializer.save()
        user = student.user
        # Get section_promo (class name) from request data
        class_id = student.section_promo.id
        if not class_id:
            return Response({"error": "section_promo (class ID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create folder with user ID inside the section_promo directory
        folder_path = os.path.join(settings.MEDIA_ROOT, class_instance.name, str(student.id))
        os.makedirs(folder_path, exist_ok=True)
        if user is not None:
            login(request, user)
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
  


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Get the user manually
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check password using `check_password`
        if check_password(password, user.password):
            login(request, user)
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)    