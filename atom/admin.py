from django.contrib import admin
from .models import LaborGroup, LaborItem, LaborClass

admin.site.register(LaborGroup)
admin.site.register(LaborItem)
admin.site.register(LaborClass)
