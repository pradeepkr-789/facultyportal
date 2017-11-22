from django.contrib import admin

# Register your models here.
from faculty.models import student,department,faculty_profile,thesis,project,recognitions

admin.site.register(student)
admin.site.register(department)
admin.site.register(faculty_profile)
admin.site.register(thesis)
admin.site.register(project)
admin.site.register(recognitions)