import datetime
from django.db import models
from django.contrib.auth.models import User
from atom.models import LaborItem, LaborClass


class PayPeriod(models.Model):
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return "%s through %s." % (self.start,
            self.end)


class Timecard(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)
    submission_notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_total_tasks_duration(self):
        """Return the total time duration of all tasks in hours as a float."""
        total = 0
        for task in Task.objects.filter(timecard__pk=self.id):
            total += task.get_task_duration()
        return total
        del total

    @property
    def is_past_due(self):
        if datetime.date.today() > self.pay_period.end:
            return True
        return False

    def __str__(self):
        return "%s, %s through %s." % (self.employee.first_name, self.pay_period.start,
            self.pay_period.end)

    class Meta:
        permissions = (
            ('can_review_timecards', "Can review timecards"),
            )

class Task(models.Model):
    timecard = models.ForeignKey(Timecard, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('hq.Project', on_delete=models.CASCADE)
    description = models.TextField()
    started = models.DateTimeField()
    finished = models.DateTimeField()
    labor_item_number = models.ForeignKey(LaborItem, on_delete=models.CASCADE)
    li_class = models.ForeignKey(LaborClass, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_task_duration(self):
        """Return the task duration in hours as a float"""
        duration = round((self.finished - self.started).seconds / 3600, 2)
        if duration > 8:
            return duration - 0.5
        return duration

    def __str__(self):
        return "%s, %s (%s)" % (self.employee.first_name, self.description, self.started)
