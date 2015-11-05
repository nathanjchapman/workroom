from django.http import Http404
from django.shortcuts import render, render_to_response
from .models import Project, Timecard, Task

def overview(request):
    tc = Timecard.objects.get()
    return render_to_response('timecards/overview.html', {'timecard': tc})

def detail(request, timecard_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
    except Timecard.DoesNotExist:
        raise Http404("Timecard does not exist.")
    return render_to_response('timecards/detail.html', {'timecard': tc})
