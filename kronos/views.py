from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Timecard, Task
from django.contrib.auth.models import User
from hq import models as hq_models
from atom.models import LaborGroup, LaborItem, LaborClass
from django.db.models import Sum

@login_required(login_url="/login/")
def overview(request):
    """/kronos/
    Return overview render.
    """
    tcss = Timecard.objects.all().filter(employee=request.user)
    tcs = tcss.filter(complete=False)
    ctcs = tcss.order_by('-pay_period_start').filter(complete=True)[:3]
    return render(request, 'kronos/overview.html', {
        'timecards': tcs,
        'complete_timecards': ctcs
        })

@login_required(login_url="/login/")
def timecard_add(request):
    """/kronos/timecard/add/
    If POST, process data and create timecard.
    """
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
def timecard_detail(request, timecard_id):
    """/kronos/1/
    Return timecard detail render.
    """
    tc = Timecard.objects.get(pk=timecard_id)
    tasks = Task.objects.all().filter(timecard=tc).order_by('date')

    return render(request, 'kronos/timecard_detail.html', {
        'timecard': tc,
        'tasks': tasks
        })

@login_required(login_url="/login/")
def timecard_complete(request, timecard_id):
    """/kronos/1/complete/
    Have to be a manager.
    If POST process data.
    """
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
def timecard_review(request, timecard_id):
    """/kronos/1/review/
    Have to be a manager.
    If POST, timecard_id, mark timecard as reviewed.
    """
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
def timecard_complete_index(request):
    """/kronos/complete/
    Return a list of completed timecards.
    """
    try:
        tc = Timecard.objects.order_by('-pay_period_start').filter(complete=True, employee=request.user)
    except Timecard.DoesNotExist:
        raise Http404("No timecards does not exist.")
    return render(request, 'kronos/timecard_complete.html', {'timecards': tc})

@permission_required('kronos.can_review_timecards')
@login_required(login_url="/login/")
def timecard_index(request):
    """/kronos/timecards/
    Return a list of all timecards.
    """
    try:
        tcs = Timecard.objects.order_by('-pay_period_start')
    except Timecard.DoesNotExist:
        raise Http404("Timecards do not exist.")
    return render(request, 'kronos/timecard_index.html', {'timecards': tcs})

@login_required(login_url="/login/")
def timecard_update(request, timecard_id):
    pass

@login_required(login_url="/login/")
def task_add(request, timecard_id):
    """/kronos/task/add/
    If POST process data and add task to timecard.
    """
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
def timecard_delete(request, timecard_id):
    """/kronos/1/delete/
    Deletes the timecard with id.
    """
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
def task_delete(request, timecard_id, task_id):
    """/kronos/1/task/1/delete/
    Delete the task with id.
    """
    t = Task.objects.get(pk=task_id)
    t.delete()
    return HttpResponseRedirect('/kronos/') 
