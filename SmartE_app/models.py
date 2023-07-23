from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class Membership(models.Model):
    membership_choices = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    type = models.CharField(unique=True, choices=membership_choices, primary_key=True, max_length=20)
    price = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.type



class Student(User):
    sid = models.BigIntegerField(primary_key=True, unique=True)
    membership = models.ForeignKey(Membership,  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Student"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    money = models.PositiveIntegerField()


class Professor(User):
    pid = models.BigIntegerField(primary_key=True, unique=True)
    class Meta:
        verbose_name = "Professor"


class Admin(User):
    is_staff = True


class Courses(models.Model):
    course_id = models.CharField(primary_key=True, unique=True, max_length=20)
    name = models.CharField(unique=True, max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, related_name='students_to_course')
    professors = models.ManyToManyField(User)
    membership_access_level = models.ForeignKey(Membership,  on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.course_id


class CourseModules(models.Model):
    module_name = models.CharField(max_length=30)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    content = models.TextField(default='')
    #files = models.FileField(upload_to='course_files/', blank=True, null=True)

    def __str__(self):
        return self.module_name

class FilesStorage(models.Model):
    module = models.ForeignKey(CourseModules, on_delete=models.CASCADE)
    file = models.FileField(upload_to="module/course_files")

    def __str__(self):
        return f"{self.module.module_name} - {self.file.name}"


class ModuleProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(CourseModules, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)  # True if student viewed the module, False otherwise

    def _str_(self):
        return f"{self.student} - {self.module}"


class ProgressTracker(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    progress = models.ManyToManyField(ModuleProgress)
    # Same can be done for grades
    grades = models.JSONField(null=True)

class Attendance(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.JSONField(null=True)

    class Meta:
        unique_together = ('course', 'student')

    def add_attendance(self, week_num: int, attended: bool):
        if self.attendance:
            self.attendance[week_num] = attended
            self.save()
        else:
            self.attendance = {week_num: attended}
    def attendance_percentage(self):
        count = 0
        if self.attendance:
            for k in self.attendance:
                if self.attendance[k] == "True":
                    count+=1
            return int(count/len(self.attendance) * 100)
        return 0
