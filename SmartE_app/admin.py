from django.contrib import admin
from SmartE_app.models import Membership, Courses, CourseModules, Student, Professor, FilesStorage, Attendance

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    pass

class ProfessorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attendance)
admin.site.register(Membership)
admin.site.register(Courses)
admin.site.register(CourseModules)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(FilesStorage)