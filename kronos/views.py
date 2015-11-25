from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Timecard, Task
from django.contrib.auth.models import User
from hq import models as hq_models
from atom.models import LaborGroup, LaborItem, LaborClass
from django.db.models import Sum

# /kronos/
# Overview of kronos
@login_required(login_url="/login/")
def overview(request):
    tcss = Timecard.objects.all().filter(employee=request.user)
    tcs = tcss.filter(complete=False)
    ctcs = tcss.order_by('-pay_period_start').filter(complete=True)[:3]
    return render(request, 'kronos/overview.html', {
        'timecards': tcs,
        'complete_timecards': ctcs
        })


@login_required(login_url="/login/")
# /kronos/timecard/add/
def timecard_add(request):
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

        return HttpResponseRedirect('/kronos/%s' % (tc.id))

    else:
        return render(request, 'kronos/timecard_add.html')


@login_required(login_url="/login/")
# /kronos/1/
def timecard_detail(request, timecard_id):
    tc = Timecard.objects.get(pk=timecard_id)
    tasks = Task.objects.all().filter(timecard=tc).order_by('date')

    return render(request, 'kronos/timecard_detail.html', {
        'timecard': tc,
        'tasks': tasks
        })


@login_required(login_url="/login/")
# /kronos/1/complete/
# have to be a manager
def timecard_complete(request, timecard_id):
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
        return render(request, 'kronos/timecard_review.html', {
            'timecard': tc,
            'tasks': tasks
            })


@permission_required('kronos.can_review_timecards')
@login_required(login_url="/login/")
# /kronos/1/review/
# have to be a manager
def timecard_review(request, timecard_id):
    # if POST process data
    if request.method == "POST":
        tc = Timecard.objects.get(pk=timecard_id)
        tc.reviewed = True
        tc.save()

        return HttpResponseRedirect('/kronos/')
    else:
        try:
            tc = Timecard.objects.get(pk=timecard_id)
            tasks = Task.objects.all().filter(timecard=tc).order_by('date')
        except Timecard.DoesNotExist:
            raise Http404("Timecard does not exist.")
        return render(request, 'kronos/timecard_review.html', {
            'timecard': tc,
            'tasks': tasks
            })


@login_required(login_url="/login/")
# /kronos/complete/
# return a list of completed timecards
def timecard_complete_index(request):
    try:
        tc = Timecard.objects.order_by('-pay_period_start').filter(complete=True)
    except Timecard.DoesNotExist:
        raise Http404("No timecards does not exist.")
    return render(request, 'kronos/timecard_complete.html', {'timecards': tc})

@permission_required('kronos.can_review_timecards')
@login_required(login_url="/login/")
# /kronos/timecards/
# return a list of all timecards
def timecard_index(request):
    try:
        tcs = Timecard.objects.order_by('-pay_period_start')
    except Timecard.DoesNotExist:
        raise Http404("Timecards do not exist.")
    return render(request, 'kronos/timecard_index.html', {'timecards': tcs})

@login_required(login_url="/login/")
def timecard_update(request, timecard_id):
    pass

@login_required(login_url="/login/")
# /kronos/task/add/
def task_add(request, timecard_id):
    # if POST process data and create timecard
    if request.method == "POST":
        employee = request.POST["employee"]
        date = request.POST["date"]
        pr = request.POST["project"]
        description = request.POST["description"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        labor_item_id = request.POST["labor_item_number"]
        li_class_id = request.POST["li_class"]

        project = hq_models.Project.objects.get(id=pr)
        user = User.objects.get(id=employee)
        timecard = Timecard.objects.get(id=timecard_id)
        labor_item = LaborItem.objects.get(id=labor_item_id)
        li_class = LaborClass(id=li_class_id)



        t = Task.objects.create(
            employee=user,
            timecard=timecard,
            date = date,
            project = project,
            description = description,
            start_time = start_time,
            end_time = end_time,
            labor_item_number = labor_item,
            li_class = li_class
            )
        t.save()

        return HttpResponseRedirect('/kronos/%s' % (timecard_id))

    else:
        li_classes = LaborClass.objects.all()
        labor_groups = LaborGroup.objects.all()
        p = hq_models.Project.objects.all().filter(archived=False)
        return render(request, 'kronos/task_add.html', {
            'projects': p,
            'timecard_id': timecard_id,
            'labor_groups': labor_groups,
            'li_classes': li_classes
            })

@login_required(login_url="/login/")
# /kronos/1/delete/
# deletes the timecard with id
def timecard_delete(request, timecard_id):
    t = Timecard.objects.get(pk=timecard_id)
    t.delete()
    return HttpResponseRedirect('/kronos/')    

@login_required(login_url="/login/")
def task_detail(request, timecard_id, task_id):
    try:
        tc = Timecard.objects.get(pk=timecard_id)
        task = Task.objects.get(pk=task_id)
    except Timecard.DoesNotExist:
        raise Http404("Task does not exist.")
    return render(request, 'kronos/task_detail.html', {
        'timecard': tc,
        'task': task
        })


@login_required(login_url="/login/")
# /kronos/1/task/1/delete/
# delete the task with id
def task_delete(request, timecard_id, task_id):
    t = Task.objects.get(pk=task_id)
    t.delete()
    return HttpResponseRedirect('/kronos/') 
