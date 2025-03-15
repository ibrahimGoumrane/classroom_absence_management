from django.contrib import admin
from .models import Subject
# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name', 'teacher__user__firstName', 'teacher__user__lastName')
    list_filter = ('teacher',)

admin.site.register(Subject, SubjectAdmin)
