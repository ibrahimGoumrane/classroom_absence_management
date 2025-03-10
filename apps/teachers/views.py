from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher
from .serializer import TeacherSerializer
from apps.users.serializer import UserSerializer


# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


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