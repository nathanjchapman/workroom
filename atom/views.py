from django.shortcuts import render
from .models import LaborGroup, LaborItem, LaborIndustryClass

def overview(request):
    li_classes = LaborIndustryClass.objects.all()
    return render(request, 'atom/overview.html', {'li_classes': li_classes})

def li_class_add(request):
    pass

def li_number_add(request):
    pass
