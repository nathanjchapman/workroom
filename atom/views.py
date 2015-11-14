from django.shortcuts import render
from .models import LaborGroup, LaborItem, LaborIndustryClass

def overview(request):
    labor_groups = LaborGroup.objects.all()
    li_classes = LaborIndustryClass.objects.all()
    return render(request, 'atom/overview.html', {
        'li_classes': li_classes,
        'labor_groups': labor_groups
        })

def li_group_add(request):
    pass

def li_class_add(request):
    pass

def li_number_add(request):
    pass
