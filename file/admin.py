from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'dob', 'salary']

admin.site.register(Employee, EmployeeAdmin)
