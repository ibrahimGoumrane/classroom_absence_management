from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher
from .serializer import TeacherSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from apps.users.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializer import UserSerializer
from apps.users.models import User
from rest_framework import serializers



# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]  # Require admin permissions for create, update, and delete


    def create(self, request, *args, **kwargs):
        teacher_serializer = self.get_serializer(data=request.data)  # Now it accepts full `user` data
        teacher_serializer.is_valid(raise_exception=True)
        teacher = teacher_serializer.save()

        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        teacher_instance = self.get_object()

        user_data = request.data.pop('user', None)  # Extract user data safely

        if user_data:
            user = teacher_instance.user
            new_email = user_data.get('email', user.email)  # Default to current email

            # ✅ Check if email is actually changing before validation
            if new_email != user.email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
                raise serializers.ValidationError({"user": {"email": ["This email is already taken by another user."]}})

            # Update user data
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # ✅ Now validate and update the teacher instance
        teacher_serializer = self.get_serializer(teacher_instance, data=request.data, partial=True)
        teacher_serializer.is_valid(raise_exception=True)
        teacher = teacher_serializer.save()

        return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        teacher_instance = self.get_object()
        user = teacher_instance.user  # Get the associated user

        self.perform_destroy(teacher_instance)  # Delete teacher
        user.delete()  # Delete the associated user

        return Response({"message": "Teacher deleted successfully."}, status=status.HTTP_204_NO_CONTENT)