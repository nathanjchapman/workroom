from django.db import models
from django.contrib.auth.models import User

class Timecard(models.Model):
    employee = models.ForeignKey(User)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Pay-period %s through %s." % (self.pay_period_start,
            self.pay_period_end)

class Task(models.Model):
    timecard = models.ForeignKey(Timecard)
    employee = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    project = models.ForeignKey('projects.Project')
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    labor_item_number = models.CharField(max_length=128)
    li_class = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

