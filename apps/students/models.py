from django.db import models
from apps.users.models import User
from apps.classes.models import Class
import os
from django.conf import settings
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    section_promo = models.ForeignKey(Class, on_delete=models.SET_NULL, related_name="students")  # ForeignKey to Class model
    class Meta:
        db_table = 'student'  # Custom table name

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.id})"


class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
    section_promo = models.CharField(max_length=255, help_text="e.g., EngineeringCycle-2_Year-Class_A")
    image = models.ImageField(upload_to='training/', max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_image'
        verbose_name = 'Student Image'
        verbose_name_plural = 'Student Images'

    def __str__(self):
        return f"Image for {self.student.user.email} in {self.section_promo}"

    def save(self, *args, **kwargs):
        if self.student and self.section_promo:
            class_name = self.student.section_promo.name
            folder_path = os.path.join(settings.MEDIA_ROOT, class_name, str(self.student.user.id))
            self.image.field.upload_to = folder_path
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        self.image.delete(save=False)
        # Call the superclass delete method to delete the record from the database
        super().delete(*args, **kwargs)