from django.contrib import admin
from .models import PayPeriod, Timecard, Task

admin.site.register(PayPeriod)
admin.site.register(Timecard)
admin.site.register(Task)
