import datetime
from django.db import transaction
from jsonschema import ValidationError
from  rest_framework import viewsets

from apps.students.models import Student
from apps.subjects.models import Subject
from .models import Attendance
from .serializer import AttendanceReadSerializer, AttendanceWriteSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from apps.users.permissions import IsTeacherOrAdmin, TeacherObjectOwnerOrAdmin, TeacherOwnObjects , IsAdmin ,IsTeacher
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from detector import FaceRecognitionHandler, imageException
from pathlib import Path
import tempfile
# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    def get_serializer_class(self):
        """Use different serializers for read/write operations"""
        if self.action in ['create', 'update', 'partial_update']:
            return AttendanceWriteSerializer
        return AttendanceReadSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow anyone to view teachers
            return [AllowAny()]
        # For create require authentication
        elif self.action == 'create':
            return [IsAuthenticated() , IsTeacherOrAdmin()] 
        # For  update, and delete actions, require either admin or teacher permissions
        return [IsAuthenticated(), TeacherObjectOwnerOrAdmin()]  


class AttendanceProcessView(viewsets.ViewSet):
    def post(self, request):
        """
        POST endpoint to process attendance by recognizing faces in uploaded images.
        Expects 'images[]', 'promo_section', and 'date' in the request body.
        """
        try:
            # Get request parameters from the body
            images = request.FILES.getlist('images[]')
            promo_section = request.data.get('promo_section')
            date = request.data.get('date')

            # Validate input parameters
            if not all([images, promo_section, date]):
                return Response(
                    {"error": "Missing required parameters: images[], promo_section, and date are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use promo_section directly as the_classe (e.g., "PROMO_IAGI_2026")
            the_classe = promo_section

            # Initialize face recognition handler
            face_handler = FaceRecognitionHandler()

            # Dictionary to store attendance results
            attendance_results = {}

            # Process each uploaded image
            with tempfile.TemporaryDirectory() as temp_dir:
                for image_file in images:
                    # Save temporary file
                    temp_path = Path(temp_dir) / image_file.name
                    with open(temp_path, 'wb+') as temp_file:
                        for chunk in image_file.chunks():
                            temp_file.write(chunk)

                    try:
                        # Recognize faces in the image
                        recognized_people = face_handler.recognize_faces(temp_path, the_classe)

                        # Process recognition results
                        for person in recognized_people:
                            attendance_results[person] = "present"

                    except imageException as e:
                        return Response(
                            {"error": f"Image processing failed: {str(e)}. Please upload a clearer image."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Get all expected students from encodings directory
            encodings_path = Path("encoding") / the_classe
            all_students = []
            if encodings_path.exists():
                for encoding_file in encodings_path.glob('*_encodings.pkl'):
                    student_id = encoding_file.stem.replace('_encodings', '')
                    all_students.append(student_id)

            student = Student.objects.get(id=student_id)  # Get the student object
            user_first_name = student.user.firstName
            user_last_name = student.user.lastName
            
            # Create final attendance list
            final_attendance = [
                {"id": student_id,"name":user_first_name+' '+user_last_name, "status": "present" if student in attendance_results else "absent"}
                for student in all_students
            ]

            # Return response
            return Response({
                "date": date,
                "promo_section": promo_section,
                "students": final_attendance
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GenerateEncodingsView(viewsets.ViewSet):
    def post(self, request):
        """
        POST endpoint to generate encodings for a specific promo_section.
        Expects 'promo_section' (e.g., 'PROMO_IAGI_2026') in the request body.
        """
        try:
            # Get promo_section from the request body
            promo_section = request.data.get('promo_section')

            # Validate input parameter
            if not promo_section:
                return Response(
                    {"error": "Missing required parameter: promo_section is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use promo_section directly as the_classe (e.g., "PROMO_IAGI_2026")
            the_classe = promo_section

            # Check if the corresponding training directory exists
            training_path = Path("training") / the_classe
            if not training_path.exists():
                return Response(
                    {"error": f"No training data found for {the_classe}. Ensure images are in training/{the_classe}/student_id/"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Initialize face recognition handler
            face_handler = FaceRecognitionHandler()

            # Generate encodings
            try:
                face_handler.encode_known_faces()
            except Exception as e:
                return Response(
                    {"error": f"Failed to generate encodings: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Verify that encodings were generated
            encodings_path = Path("encoding") / the_classe
            generated_files = list(encodings_path.glob('*_encodings.pkl')) if encodings_path.exists() else []
            if not generated_files:
                return Response(
                    {"error": f"No encodings were generated for {the_classe}. Ensure images contain detectable faces."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                "message": f"Encodings generated successfully for {the_classe}",
                "encoding_path": str(encodings_path),
                "generated_files": [file.name for file in generated_files]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class AttendanceConfirmView(viewsets.ViewSet):
    def post(self, request):
        """
        POST - Confirm and Store Attendance
        Endpoint: /api/attendance/confirm
        Description:
        The request takes a JSON list containing students, subject, date, and status.
        After processing, this data is stored in the database.
        Request Body Format:
        {
            "date": "YYYY-MM-DD",
            "subject": "Mathematics",
            "students": [
                {
                    "student_id": "123",
                    "status": "present"
                },
                {
                    "student_id": "456",
                    "status": "absent"
                }
            ]
        }
        Response:
        {
            "message": "Attendance successfully recorded",
            "status": "success",
            "records_processed": 2
        }
        """
        try:
            # Extract data from request
            data = request.data
            date_str = data.get('date')
            subject_name = data.get('subject')
            students_data = data.get('students')

            # Validate required fields
            if not all([date_str, subject_name, students_data]):
                return Response(
                    {"error": "Missing required fields: date, subject, and students are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate date format
            try:
                attendance_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate subject name (basic check for non-empty and no special characters)
            if not subject_name.strip() or not subject_name.isalnum() and '_' not in subject_name:
                return Response(
                    {"error": "Subject name must be non-empty and contain only alphanumeric characters or underscores"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate students data is a list
            if not isinstance(students_data, list):
                return Response(
                    {"error": "Students must be provided as a list"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use Django's transaction to ensure atomicity
            with transaction.atomic():
                # Get or create subject
                try:
                    subject = Subject.objects.get(name=subject_name)
                except Subject.DoesNotExist:
                    return Response(
                        {"error": f"Subject '{subject_name}' not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Process each student
                records_processed = 0
                for student_entry in students_data:
                    student_id = student_entry.get('student_id')
                    status_value = student_entry.get('status')

                    # Validate student entry
                    if not all([student_id, status_value]):
                        return Response(
                            {"error": "Each student entry must have student_id and status"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    if status_value not in ['present', 'absent']:
                        return Response(
                            {"error": f"Invalid status '{status_value}' for student {student_id}. Must be 'present' or 'absent'"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Get student by student_id (assuming Student model has an id field)
                    try:
                        student = Student.objects.get(id=student_id)
                    except Student.DoesNotExist:
                        return Response(
                            {"error": f"Student with student_id {student_id} not found"},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    # Create or update attendance record
                    Attendance.objects.update_or_create(
                        student=student,
                        subject=subject,
                        date=attendance_date,
                        defaults={'status': status_value}
                    )
                    records_processed += 1

                # Success response
                return Response(
                    {
                        "message": "Attendance successfully recorded",
                        "status": "success",
                        "records_processed": records_processed
                    },
                    status=status.HTTP_201_CREATED
                )

        except ValidationError as e:
            return Response(
                {"error": f"Validation error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )