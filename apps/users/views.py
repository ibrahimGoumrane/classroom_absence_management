from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import os

from .models import User
from .serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def perform_create(self, serializer):
        # Automatically hash the password when creating a user
        user = serializer.save()
        user.set_password(user.password)  # Hash the password
        user.save()

# Folder creation (admin-only)
class FolderCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # if request.user.role.lower() != 'admin':
        #     return Response(
        #         {"error": "Only admins can create folders"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        cycle = request.data.get('cycle')
        year = request.data.get('year')
        class_name = request.data.get('class_name')

        if not all([cycle, year, class_name]):
            return Response(
                {"error": "Missing required fields: cycle, year, class_name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_name = f"{cycle}-{year}_Year-Class_{class_name}"
        folder_path = os.path.join(settings.BASE_DIR, 'training', folder_name)

        try:
            os.makedirs(folder_path, exist_ok=True)
            return Response(
                {"message": f"Folder '{folder_name}' created successfully"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create folder: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )