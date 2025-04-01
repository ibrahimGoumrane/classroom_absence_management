from django.db import models
from apps.users.models import User
from apps.departments.models import Department


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teachers")
    
    class Meta:
        db_table = 'teacher'  # Custom table name

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} : ({self.department})"
