from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Student, StudentImage
from .serializer import StudentImageSerializer
import os
from django.conf import settings
# from rest_framework.permissions import AllowAny


class UploadStudentImagesView(ModelViewSet):
    queryset = StudentImage.objects.all()
    serializer_class = StudentImageSerializer
    def get_permissions(self):
        return [IsAuthenticated()]
    

    def list(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')

        if student_id:
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

        images = StudentImage.objects.filter(student=student)
        serializer = StudentImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        images = request.FILES.getlist('images')
        # use the id of the user to get the student
        # student = Student.objects.get(user=user)
        print(user.role.lower())
        if user.role.lower() in ['admin', 'student']:
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
            
        created_images = []
        for image in images:
            created_image = StudentImage.objects.create(student=student, image=image)
            created_images.append(created_image)  
        serializer = StudentImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        user = request.user
        if user.role.lower() not in ['admin','student'] and user.id != image.student.user.id:
            return Response({"error": "You are not authorized to delete this image"}, status=status.HTTP_403_FORBIDDEN)

        image_path = os.path.join(settings.MEDIA_ROOT,image.image.path)
        
        image.delete()

        if os.path.exists(image_path):
            os.remove(image_path)

        return Response({"message": "Image deleted successfully"}, status=status.HTTP_200_OK)
