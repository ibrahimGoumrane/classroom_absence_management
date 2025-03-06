from django.db import models
from apps.users.models import User
# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    cycle = models.CharField(max_length=100)
    year = models.IntegerField()
    department = models.CharField(max_length=100)
    class Meta:
        db_table = 'student'  # Custom table name
    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.student_id})"