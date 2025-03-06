from django.db import models
from apps.users.models import User

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.CharField(max_length=100)
    class Meta:
        db_table = 'teacher'  # Custom table name
    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.teacher_id})"
