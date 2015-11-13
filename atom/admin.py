from django.contrib import admin
from .models import LaborGroup, LaborItem, LaborIndustryClass

admin.site.register(LaborGroup)
admin.site.register(LaborItem)
admin.site.register(LaborIndustryClass)
