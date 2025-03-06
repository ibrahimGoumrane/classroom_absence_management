from django.db import models
from apps.teachers.models import Teacher

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="subjects")

    def __str__(self):
        return f"{self.name} ({self.code})"