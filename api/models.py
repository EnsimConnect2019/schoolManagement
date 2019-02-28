from django.contrib.auth.models import User, Group
from django.db import models
from django_mysql.models import EnumField


def get_first_name(self):
    first_name = models.CharField(unique=True, max_length=20)
    return self.first_name

    User.add_to_class("__str__", get_first_name)

# class MyUser(User):#
#     def __str__(self):
#         return self.first_name

# Student Parent relationship table
class ChildParentsRelation(models.Model):
    student = models.ForeignKey(User, null=True, related_name='assignee', on_delete=models.CASCADE)
    parent = models.ForeignKey(User, null=True, related_name='creator', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'parent')


# Class room no. table
class ClassRoom(models.Model):
    class_room_name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.class_room_name


# Subjects Table
class Subject(models.Model):
    subject_name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.subject_name


# Classes Table
class ClassName(models.Model):
    class_text = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.class_text


# Class and Subject relations Table
class ClassSubject(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_name', 'subject')


# Student and Class Relation Table
class StudentClass(models.Model):
    roll_no = models.BigIntegerField(null=False)
    session_year = models.CharField(max_length=4, help_text="Year of Session")
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('roll_no', 'class_name', 'session_year')

    def __str__(self):
        return self.session_year


# Basic Schedule Template
class ScheduleTemplate(models.Model):
    day = EnumField(choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.day


# Daily Schedules update
class Schedule(models.Model):
    schedule_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=200)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


# Holiday List Table
class Holiday(models.Model):
    holiday_title = models.CharField(max_length=200)
    celebrate_on = models.DateField()

    def __str__(self):
        return self.holiday_title


# Student's Attendance Table

class Attendance(models.Model):
    present = EnumField(choices=['Yes', 'No'])
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.present
