from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Student, StudentImage
from .serializer import StudentSerializer,StudentImageSerializer
import os
from django.conf import settings
from apps.users.serializer import UserSerializer
from apps.classes.models import Class

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    # This method is overridden to create a folder with the user ID inside the section_promo directory and create a user then create a student
    def create(self, request, *args, **kwargs):
        # Extract user data from request
        user_data = request.data.pop('user')
        
        # Create user
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        # Get section_promo (class name) from request data
        class_id = request.data.get('section_promo')
        if not class_id:
            return Response({"error": "section_promo (class ID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create folder with user ID inside the section_promo directory
        folder_path = os.path.join(settings.MEDIA_ROOT, class_instance.name, str(user.id))
        os.makedirs(folder_path, exist_ok=True)
        
        # Create student with the created user
        request.data['user'] = user.id
        response = super().create(request, *args, **kwargs)
        
        return response
    
    # We will override the update method to update te user then the student
    def update(self, request, *args, **kwargs):
        # Extract user data from request
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
    


class UploadStudentImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role.lower() == 'admin':
            student_id = request.query_params.get('student_id')
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                except Student.DoesNotExist:
                    return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
                images = StudentImage.objects.filter(student=student)
            else:
                return Response({"error": "student_id parameter is required for admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                student = Student.objects.get(user=user)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
            images = StudentImage.objects.filter(student=student)

        serializer = StudentImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        images = request.FILES.getlist('images')
        if not user :
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        student = Student.objects.get(user=user)

        if user.role.lower() == 'admin':
            student_id = request.data.get('student_id')

            if not all([ student_id, images]):
                return Response({"error": "Missing required fields: student_id, images"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        else: 
            if not all([images]):
                return Response({"error": "Missing required fields:  images"}, status=status.HTTP_400_BAD_REQUEST)
            

        for image in images:
            StudentImage.objects.create(student=student,image=image)
        return Response({"message": "Images uploaded successfully"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        user = request.user
        if not user :
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        image_id = request.data.get('image_id')
        if not image_id:
            return Response({"error": "image_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = StudentImage.objects.get(id=image_id)
        except StudentImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.id != image.student.user.id:
            return Response({"error": "You are not authorized to delete this image"}, status=status.HTTP_403_FORBIDDEN)


        image.delete()

        return Response({"message": "Image deleted successfully"}, status=status.HTTP_200_OK)

