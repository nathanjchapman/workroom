import datetime
from django.db import models
from django.contrib.auth.models import User
from atom.models import LaborItem, LaborClass
from datetime import date, timedelta

class Timecard(models.Model):
    employee = models.ForeignKey(User)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    submission_notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def is_past_due(self):
        if date.today() > self.pay_period_end:
            return True
        return False

    def __str__(self):
        return "Pay-period %s through %s." % (self.pay_period_start,
            self.pay_period_end)

    class Meta:
        permissions = (
            ('can_review_timecards', "Can review timecards"),
            )

class Task(models.Model):
    timecard = models.ForeignKey(Timecard)
    employee = models.ForeignKey(User)
    date = models.DateField()
    project = models.ForeignKey('hq.Project')
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    labor_item_number = models.ForeignKey(LaborItem)
    li_class = models.ForeignKey(LaborClass)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_hours(self):
        # returns time in hours as a float
        return (self.end_time - self.start_time).seconds / 3600

    def __str__(self):
        return self.description
