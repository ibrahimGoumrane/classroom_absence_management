from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher
from .serializer import TeacherSerializer
from apps.users.serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        user_data = request.data.pop('user')

        # create user
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Create teacher with the created user
        request.data['user'] = user.id
        response = super().create(request, *args, **kwargs)
        
        return response
    
    def update(self, request, *args, **kwargs):
        user_data = request.data.pop('user')

        # Get the existing teacher instance
        teacher_instance = self.get_object()

        # Update the user
        user_serializer = UserSerializer(teacher_instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Update the teacher
        request.data['user'] = user_serializer.data['id']
        response = super().update(request, *args, **kwargs)
        return response
