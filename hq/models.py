from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=72)
    city = models.CharField(max_length=72)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "%s, %s, %s" % (self.street, self.city, self.state)

    class Meta:
        verbose_name_plural = "addresses"

class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    address = models.ManyToManyField(Address)
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

