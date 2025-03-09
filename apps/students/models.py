from django.db import models
from apps.users.models import User

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    cycle = models.CharField(max_length=100)
    year = models.IntegerField()
    department = models.CharField(max_length=100)

    class Meta:
        db_table = 'student'  # Custom table name

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.id})"


class StudentImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
    promo_section = models.CharField(max_length=255, help_text="e.g., EngineeringCycle-2_Year-Class_A")
    image = models.ImageField(upload_to='training/', max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_image'
        verbose_name = 'Student Image'
        verbose_name_plural = 'Student Images'

    def __str__(self):
        return f"Image for {self.student.user.email} in {self.promo_section}"

    def save(self, *args, **kwargs):
        if self.student and self.promo_section:
            self.image.field.upload_to = f'training/{self.promo_section}/{self.student.id}/'
        super().save(*args, **kwargs)