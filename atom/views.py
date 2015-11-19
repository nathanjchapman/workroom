from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import LaborGroup, LaborItem, LaborClass

@login_required(login_url="/login/")
def overview(request):
    labor_groups = LaborGroup.objects.all()
    labor_classes = LaborClass.objects.all()
    return render(request, 'atom/overview.html', {
        'labor_classes': labor_classes,
        'labor_groups': labor_groups
        })

@login_required(login_url="/login/")
def labor_class_add(request):
    pass

@login_required(login_url="/login/")
def labor_group_add(request):
    pass

@login_required(login_url="/login/")
def labor_item_add(request):
    pass
