from django.contrib import admin

# Register your models here.
from faculty.models import student,department,faculty_profile,project,recognition,publication,teaching,workexperience

admin.site.register(student)
admin.site.register(department)
admin.site.register(faculty_profile)
admin.site.register(project)
admin.site.register(recognition)
admin.site.register(publication)
admin.site.register(teaching)
admin.site.register(workexperience)