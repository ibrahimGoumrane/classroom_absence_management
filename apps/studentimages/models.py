from django.db import models
from apps.students.models import Student
import os
from django.conf import settings
import uuid


def student_image_upload_path(instance, filename):
    """
    Generates a safe upload path for student images.
    - Prevents directory traversal attacks.
    - Organizes images in `MEDIA_ROOT/training/{section_promo}/{student_id}/filename`.
    """
    ext = filename.split('.')[-1]  # Extract file extension
    new_filename = f"{uuid.uuid4().hex}.{ext}"  # Generate a unique filename

    if instance.student:
        class_name = instance.student.section_promo.name  # Assuming section_promo is a related field
        return os.path.join(class_name, str(instance.student.id), new_filename)


class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=student_image_upload_path, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_encoded = models.BooleanField(default=False)

    class Meta:
        db_table = 'student_image'
        verbose_name = 'Student Image'
        verbose_name_plural = 'Student Images'

    def __str__(self):
        return f"Image for {self.student.user.email} in {self.student.section_promo.name}"

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)  # Call Django's delete method
