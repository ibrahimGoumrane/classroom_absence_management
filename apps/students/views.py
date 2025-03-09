from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Student, StudentImage
from .serializer import StudentSerializer,StudentImageSerializer


# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class UploadStudentImagesView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if user is admin
        # if request.user.role.lower() != 'admin':
        #     return Response(
        #         {"error": "Only admins can upload images"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        promo_section = request.data.get('promo_section')
        student_id = request.data.get('student_id')
        images = request.FILES.getlist('images')  # Expect multipart file uploads

        if not all([promo_section, student_id, images]):
            return Response(
                {"error": "Missing required fields: promo_section, student_id, images"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Save each image
        for image in images:
            StudentImage.objects.create(student=student, promo_section=promo_section, image=image)

        return Response({"message": "Images uploaded successfully"}, status=status.HTTP_201_CREATED)