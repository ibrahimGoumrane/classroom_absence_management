from django.contrib import admin
from .models import Attendance
# Register your models here.
# Admin class for Attendance model
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status')
    list_filter = ('status', 'date', 'subject')
    search_fields = ('student__user__firstName', 'student__user__lastName', 'subject__name')

admin.site.register(Attendance, AttendanceAdmin)  