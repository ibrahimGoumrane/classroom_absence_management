from django.contrib import admin
from .models import Student
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'section_promo')
    search_fields = ('user__firstName', 'user__lastName', 'user__email')
    list_filter = ('section_promo',)

admin.site.register(Student, StudentAdmin)