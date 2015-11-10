from django.http import Http404
from django.shortcuts import render
from .models import Timecard, Task

def overview(request):
    tc = Timecard.objects.get()
    return render_to_response('timecards/overview.html', {'timecard': tc})

def add_timecard(request):
    # if POST process data and create timecard
    if request.method == "POST"
        employee = request.POST["employee"]
        pay_period_start = request.POST["pay_period_start"]
        pay_period_end = request.POST["pay_period_end"]

        tc = Timecard.objects.create(employee=employee,
            pay_period_start=pay_period_start, pay_period_end=pay_period_end)
        tc.save()

def detail(request, timecard_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
    except Timecard.DoesNotExist:
        raise Http404("Timecard does not exist.")
    return render(request, 'timecards/detail.html', {'timecard': tc})
