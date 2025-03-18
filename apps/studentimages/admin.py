from django.contrib import admin
from .models import StudentImage
# Register your models here.
class StudentImageAdmin(admin.ModelAdmin):
    list_display = ('student', 'image', 'uploaded_at')
    search_fields = ('student__user__firstName', 'student__user__lastName', 'student__user__email')
    list_filter = ('uploaded_at',)

admin.site.register(StudentImage, StudentImageAdmin)