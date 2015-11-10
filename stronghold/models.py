from django.db import models

class Door(models.Model):
    location = models.CharField(max_length=128)
    address = models.ForeignKey('hq.Address')

    def __str__(self):
        return "%s (%s)" % (self.location, self.address)

class Code(models.Model):
    door = models.ManyToManyField(Door)
    number = models.IntegerField()
    permanent = models.BooleanField(default=False)
    belongs_to = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "%d" % (self.number)

