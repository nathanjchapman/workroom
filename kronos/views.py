from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Timecard, Task
from django.contrib.auth.models import User

def overview(request):
    tcs = Timecard.objects.all().filter(complete=False)
    return render(request, 'kronos/timecards/overview.html', {'timecards': tcs})

def add_timecard(request):
    # if POST process data and create timecard
    if request.method == "POST":
        employee = request.POST["employee"]
        pay_period_start = request.POST["pay_period_start"]
        pay_period_end = request.POST["pay_period_end"]

        user = User.objects.get(id=employee)

        tc = Timecard.objects.create(
            employee=user,
            pay_period_start=pay_period_start,
            pay_period_end=pay_period_end
            )
        tc.save()

        return HttpResponseRedirect('/kronos/')

    else:
        return render(request, 'kronos/timecards/add.html')

def detail(request, timecard_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
        tasks = Task.objects.all().filter(timecard=tc).order_by('date')
    except Timecard.DoesNotExist:
        raise Http404("Timecard does not exist.")
    return render(request, 'kronos/timecards/detail.html', {
        'timecard': tc,
        'tasks': tasks
        })

# have to be a manager
def review(request, timecard_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
    except Timecard.DoesNotExist:
        raise Http404("Timecard does not exist.")
    return render(request, 'kronos/timecards/review.html', {'timecard': tc})

def completed(request):
    pass

def update(request, timecard_id):
    pass

#def edit(request, timecard_id):


#def delete(request, timecard_id):
