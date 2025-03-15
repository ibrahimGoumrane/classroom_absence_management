from django.contrib import admin
from .models import Teacher
# Register your models here.
# Admin class for Teacher model
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__firstName', 'user__lastName', 'department')
    list_filter = ('department',)

admin.site.register(Teacher, TeacherAdmin)