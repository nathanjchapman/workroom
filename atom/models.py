from django.db import models

class LaborGroup(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=72)

    def __str__(self):
        return "%d - %s" % (self.number, self.name)

class LaborItem(models.Model):
    group = models.ForeignKey(LaborGroup)
    number = models.IntegerField()
    description = models.CharField(max_length=72)

    def __str__(self):
        return "%d %s" % (self.number, self.description)    

class LaborClass(models.Model):
    number = models.CharField(max_length=8)
    name = models.CharField(max_length=72)
    description = models.TextField(max_length=72)
    company_rate = models.DecimalField(max_digits=8, decimal_places=2)
    employee_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s %s" % (self.number, self.name)

    class Meta:
        verbose_name_plural = "labor classes"
