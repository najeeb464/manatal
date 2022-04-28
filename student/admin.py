from django.contrib import admin

# Register your models here.
from student.models import Student,School
from student.forms import StudentForm,SchoolForm

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('__str__','dob','display_gender','country')
    search_fields = ('first_name','last_name','identification','school__name')
    list_filter  = ('gender',)

class SchoolAdmin(admin.ModelAdmin):
    form = SchoolForm
    # list_display = ('__str__','max_student_limit','display_gender','city','state','country')
    # search_fields = ('first_name','last_name','identification','school__name')
    # list_filter  = ('gender',)
    
admin.site.register(School,SchoolAdmin)
admin.site.register(Student,StudentAdmin)