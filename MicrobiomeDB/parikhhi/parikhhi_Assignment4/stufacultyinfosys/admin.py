# Register your models here.

from django.contrib import admin
from stufacultyinfosys.models import Faculty
from stufacultyinfosys.models import Student
from stufacultyinfosys.models import Major
from stufacultyinfosys.models import Course


admin.site.register(Faculty)

admin.site.register(Student)

admin.site.register(Major)

admin.site.register(Course)


