from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class Student(User):
    sid = models.BigIntegerField(primary_key=True, unique=True)


class Professor(User):
    pid = models.BigIntegerField(primary_key=True, unique=True)


class Admin(User):
    is_staff = True


class Courses(models.Model):
    course_id = models.CharField(primary_key=True, unique=True)
    name = models.CharField(unique=True, max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, related_name='students_to_course')
    professors = models.ManyToManyField(Professor)


class CourseModules(models.Model):
    module_name = models.CharField(max_length=30)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


class ProgressTracker(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
