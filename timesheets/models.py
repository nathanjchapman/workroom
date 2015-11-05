from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TimeSheet(models.Model):
    employee = models.ForeignKey(User)
    pay_period = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    TimeSheet = models.ForeignKey(TimeSheet)
    employee = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    project = models.ForeignKey(Project)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    labor_item_number = models.CharField(max_length=128)
    li_class = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

