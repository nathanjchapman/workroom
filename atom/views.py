from django.shortcuts import render
from .models import LaborGroup, LaborItem, LaborClass

def overview(request):
    labor_groups = LaborGroup.objects.all()
    labor_classes = LaborClass.objects.all()
    return render(request, 'atom/overview.html', {
        'labor_classes': labor_classes,
        'labor_groups': labor_groups
        })

def labor_class_add(request):
    pass

def labor_group_add(request):
    pass

def labor_item_add(request):
    pass
