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

class Door(models.Model):
    location = models.CharField(max_length=128)
    address = models.ForeignKey(Address)

    def __str__(self):
        return "%s (%s)" % (self.location, self.address)

class Code(models.Model):
    door = models.ManyToManyField(Door)
    number = models.IntegerField()
    permanent = models.BooleanField(default=False)
    belongs_to = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "%d" % (self.number)

