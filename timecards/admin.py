from django.contrib import admin
from .models import Project, Timecard, Task

admin.site.register(Project)
admin.site.register(Timecard)
admin.site.register(Task)

