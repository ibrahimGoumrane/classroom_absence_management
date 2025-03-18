from django.db import models
from apps.users.models import User
from apps.classes.models import Class


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    section_promo = models.ForeignKey(Class, on_delete=models.SET_NULL, related_name="students" , null=True, blank=True )  # ForeignKey to Class model
    class Meta:
        db_table = 'student'  # Custom table name

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.id})"


