from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Student(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    roll_number = models.CharField(max_length=5)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    grace_marks = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    cgpa = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])


class Advisor(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])


class Faculty(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Faculties'


class Course(models.Model):
    course_title = models.CharField(primary_key=True, max_length=10)
    year = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])


class FacultyCourse(models.Model):
    username = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE)


class Coe(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    grace_mark_applied = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Coe'


class Grade(models.Model):
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE)
    fromA = models.IntegerField(default=85, validators=[MinValueValidator(1), MaxValueValidator(100)])
    toA = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(100)])
    fromB = models.IntegerField(default=60, validators=[MinValueValidator(1), MaxValueValidator(100)])
    toB = models.IntegerField(default=84, validators=[MinValueValidator(1), MaxValueValidator(100)])
    fromC = models.IntegerField(default=36, validators=[MinValueValidator(1), MaxValueValidator(100)])
    toC = models.IntegerField(default=59, validators=[MinValueValidator(1), MaxValueValidator(100)])
    fromF = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    toF = models.IntegerField(default=35, validators=[MinValueValidator(1), MaxValueValidator(100)])
    credits = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(4)])


class Mark(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.IntegerField(default=80, validators=[MinValueValidator(1), MaxValueValidator(100)])


class Event(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    no_of_events = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)


class BoolCheck(models.Model):
    s_no = models.IntegerField(default=1)
    grace_mark_applied = models.BooleanField(default=False)


class Lock(models.Model):
    username = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
