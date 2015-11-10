from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

