from django.contrib import admin
from .models import Project, TimeSheet, Task

admin.site.register(Project)
admin.site.register(TimeSheet)
admin.site.register(Task)

