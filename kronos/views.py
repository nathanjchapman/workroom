from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Timecard, Task
from django.contrib.auth.models import User
from hq import models as hq_models

# /kronos/
# Overview of all timecards
def overview(request):
    tcss = Timecard.objects.all().filter(employee=request.user)
    tcs = tcss.filter(complete=False)
    ctcs = tcss.order_by('-pay_period_start').filter(complete=True)[:3]
    return render(request, 'kronos/overview.html', {
        'timecards': tcs,
        'complete_timecards': ctcs
        })

# /kronos/timecard/add/
def add_timecard(request):
    # if POST process data and create timecard
    if request.method == "POST":
        pay_period_start = request.POST["pay_period_start"]
        pay_period_end = request.POST["pay_period_end"]


        tc = Timecard.objects.create(
            employee=request.user,
            pay_period_start=pay_period_start,
            pay_period_end=pay_period_end
            )
        tc.save()

        return HttpResponseRedirect('/kronos/')

    else:
        return render(request, 'kronos/addtimecard.html')

# /kronos/1/
def detail(request, timecard_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
        tasks = Task.objects.all().filter(timecard=tc).order_by('date')
    except Timecard.DoesNotExist:
        raise Http404("Timecard does not exist.")
    return render(request, 'kronos/detail.html', {
        'timecard': tc,
        'tasks': tasks
        })

# /kronos/1/review
# have to be a manager
def review(request, timecard_id):
    # if POST process data
    if request.method == "POST":
        tc = Timecard.objects.get(pk=timecard_id)
        tc.submission_notes = request.POST["submission_notes"]
        tc.complete = True
        tc.save()

        return HttpResponseRedirect('/kronos/')
    else:
        try:
            tc = Timecard.objects.get(pk=timecard_id)
            tasks = Task.objects.all().filter(timecard=tc).order_by('date')
        except Timecard.DoesNotExist:
            raise Http404("Timecard does not exist.")
        return render(request, 'kronos/review.html', {
            'timecard': tc,
            'tasks': tasks
            })

# /kronos/complete/
# return a list of completed timecards
def complete(request):
    try:
        tc = Timecard.objects.order_by('-pay_period_start').filter(complete=True)
    except Timecard.DoesNotExist:
        raise Http404("No timecards does not exist.")
    return render(request, 'kronos/complete.html', {'timecards': tc})

# /kronos/timecards/
# return a list of all timecards
def timecards(request):
    try:
        tcs = Timecard.objects.order_by('-pay_period_start')
    except Timecard.DoesNotExist:
        raise Http404("Timecards do not exist.")
    return render(request, 'kronos/timecard_index.html', {'timecards': tcs})

def update(request, timecard_id):
    pass

# /kronos/task/add/
def add_task(request, timecard_id):
    # if POST process data and create timecard
    if request.method == "POST":
        employee = request.POST["employee"]
        date = request.POST["date"]
        pr = request.POST["project"]
        description = request.POST["description"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        labor_item_number = request.POST["labor_item_number"]
        li_class = request.POST["li_class"]

        project = hq_models.Project.objects.get(id=pr)
        user = User.objects.get(id=employee)
        timecard = Timecard.objects.get(id=timecard_id)

        t = Task.objects.create(
            employee=user,
            timecard=timecard,
            date = date,
            project = project,
            description = description,
            start_time = start_time,
            end_time = end_time,
            labor_item_number = labor_item_number,
            li_class = li_class
            )
        t.save()

        return HttpResponseRedirect('/kronos/')

    else:
        p = hq_models.Project.objects.all()
        return render(request, 'kronos/addtask.html', {
            'projects': p,
            'timecard_id': timecard_id
            })

def edit(request, timecard_id):
    pass

# /kronos/1/delete/
# deletes the timecard with id
def deletetc(request, timecard_id):
    t = Timecard.objects.get(pk=timecard_id)
    t.delete()
    return HttpResponseRedirect('/kronos/')    

def detail_task(request, timecard_id, task_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
        task = Task.objects.get(pk=task_id)
    except Timecard.DoesNotExist:
        raise Http404("Task does not exist.")
    return render(request, 'kronos/detail_task.html', {
        'timecard': tc,
        'task': task
        })

# /kronos/1/task/1/delete/
# delete the task with id
def delete_task(request, timecard_id, task_id):
    t = Task.objects.get(pk=task_id)
    t.delete()
    return HttpResponseRedirect('/kronos/') 