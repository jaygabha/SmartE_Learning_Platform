from django.contrib import admin

from SmartE_app.models import Membership, Courses, CourseModules, Student

# Register your models here.

admin.site.register(Membership)
admin.site.register(Courses)
admin.site.register(CourseModules)
admin.site.register(Student)