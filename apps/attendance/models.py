from django.db import models
from apps.students.models import Student
from apps.subjects.models import Subject
from django.utils import timezone

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[("present", "Present"), ("absent", "Absent")])
    class Meta:
        db_table = 'attendance'  # Custom table name
    def __str__(self):
        return f"{self.student.user.firstName} {self.student.user.lastName}  - {self.subject.name} - {self.date} ({self.status})"