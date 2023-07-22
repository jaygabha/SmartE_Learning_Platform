from django.contrib import admin

from SmartE_app.models import Membership, Courses, Professor, Admin, Student

# Register your models here.

admin.site.register(Membership)
admin.site.register(Courses)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Admin)
