from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import Employees


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date']
    list_display_links = ['emp_no', 'first_name']
    list_filter = ('gender', ('hire_date', DateRangeFilter), ('birth_date', DateRangeFilter))
    search_fields = ['emp_no', 'first_name', 'last_name']


admin.site.register(Employees, EmployeesAdmin)
