from django.db import models

# Create your models here.

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        db_table = "classes"
