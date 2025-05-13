from django.db import models
from apps.teachers.models import Teacher
from apps.classes.models import Class

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="subjects")
    section_promo = models.ForeignKey(Class, on_delete=models.SET_NULL, related_name="classes" , null=True, blank=True )  # ForeignKey to Class model
    class Meta:
        db_table = 'subject'  # Custom table name
    def __str__(self):
        return f"{self.name}"