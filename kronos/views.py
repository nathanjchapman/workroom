from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import PayPeriod, Timecard, Task
from django.contrib.auth.models import User
from hq import models as hq_models
from atom.models import LaborGroup, LaborItem, LaborClass
from django.db.models import Sum
import datetime


@login_required(login_url="/login/")
def overview(request):
    """/kronos/
    Return overview render.
    """
    timecards = Timecard.objects.all().filter(employee=request.user, complete=False)
    return render(request, 'kronos/overview.html', {
        'timecards': timecards
        })


@login_required(login_url="/login/")
def timecard_add(request):
    """/kronos/timecard/add/
    If POST, process data and create timecard.
    """
    if request.method == "POST":
        p = request.POST["pay_period"]
        pay_period = PayPeriod.objects.get(pk=p)

        timecard = Timecard.objects.create(
            employee=request.user,
            pay_period=pay_period
            )
        timecard.save()

        return HttpResponseRedirect('/kronos/%s' % (timecard.id))

    else:
        pay_periods = PayPeriod.objects.order_by('-start')[:3]
        return render(request, 'kronos/timecard_add.html', {'pay_periods': pay_periods})


@login_required(login_url="/login/")
def timecard_detail(request, timecard_id):
    """/kronos/1/
    Return timecard detail render.
    """
    timecard = Timecard.objects.get(pk=timecard_id)
    tasks = Task.objects.all().filter(timecard=timecard).order_by('started')

    return render(request, 'kronos/timecard_detail.html', {
        'timecard': timecard,
        'tasks': tasks
        })


@login_required(login_url="/login/")
def timecard_complete(request, timecard_id):
    """/kronos/1/complete/
    Have to be a manager.
    If POST process data.
    """
    if request.method == "POST":
        timecard = Timecard.objects.get(pk=timecard_id)
        timecard.submission_notes = request.POST["submission_notes"]
        timecard.complete = True
        timecard.save()

        return HttpResponseRedirect('/kronos/')
    else:
        try:
            timecard = Timecard.objects.get(pk=timecard_id)
            tasks = Task.objects.all().filter(timecard=timecard).order_by('started')
        except Timecard.DoesNotExist:
            raise Http404("Timecard does not exist.")
        return render(request, 'kronos/timecard_review.html', {
            'timecard': timecard,
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
        timecard = Timecard.objects.get(pk=timecard_id)
        timecard.reviewed = True
        timecard.save()

        return HttpResponseRedirect('/kronos/timecards/')
    else:
        try:
            timecard = Timecard.objects.get(pk=timecard_id)
            tasks = Task.objects.all().filter(timecard=timecard).order_by('started')
        except Timecard.DoesNotExist:
            raise Http404("Timecard does not exist.")
        return render(request, 'kronos/timecard_review.html', {
            'timecard': timecard,
            'tasks': tasks
            })


@login_required(login_url="/login/")
def timecard_complete_index(request):
    """/kronos/complete/
    Return a list of completed timecards.
    """
    try:
        timecard = Timecard.objects.order_by('-pay_period').filter(complete=True, employee=request.user)
    except Timecard.DoesNotExist:
        raise Http404("No timecards does not exist.")
    return render(request, 'kronos/timecard_complete.html', {'timecards': timecard})

@permission_required('kronos.can_review_timecards')
@login_required(login_url="/login/")
def timecard_index(request):
    """/kronos/timecards/
    Return a list of all timecards.
    """
    try:
        pay_period= PayPeriod.objects.order_by('-start')
    except PayPeriod.DoesNotExist:
        raise Http404("Timecards do not exist.")
    return render(request, 'kronos/timecard_index.html', {'pay_periods': pay_period})

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
        project_id = request.POST["project"]
        description = request.POST["description"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        labor_item_id = request.POST["labor_item_number"]
        li_class_id = request.POST["li_class"]

        started = "%s %s" % (date, start_time)
        finished = "%s %s" % (date, end_time)

        project = hq_models.Project.objects.get(id=project_id)
        user = User.objects.get(id=employee)
        timecard = Timecard.objects.get(id=timecard_id)
        labor_item = LaborItem.objects.get(id=labor_item_id)
        li_class = LaborClass(id=li_class_id)

        t = Task.objects.create(
            employee=user,
            timecard=timecard,
            project = project,
            description = description,
            started = started,
            finished = finished,
            labor_item_number = labor_item,
            li_class = li_class
            )
        t.save()

        return HttpResponseRedirect('/kronos/%s' % (timecard_id))

    else:
        li_classes = LaborClass.objects.all()
        labor_groups = LaborGroup.objects.all()
        projects = hq_models.Project.objects.all().filter(archived=False)
        return render(request, 'kronos/task_add.html', {
            'projects': projects,
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
        timecard = Timecard.objects.get(pk=timecard_id)
        task = Task.objects.get(pk=task_id)
    except Timecard.DoesNotExist:
        raise Http404("Task or Timecard do not exist.")
    return render(request, 'kronos/task_detail.html', {
        'timecard': timecard,
        'task': task
        })

@login_required(login_url="/login/")
def task_update(request, timecard_id, task_id):
    """/kronos/1/task/1/update/
    Updates task with id.
    """
    if request.method == "POST":

        date = request.POST["date"]
        project_id = request.POST["project"]
        description = request.POST["description"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        labor_item_id = request.POST["labor_item_number"]
        li_class_id = request.POST["li_class"]

        started = "%s %s" % (date, start_time)
        finished = "%s %s" % (date, end_time)

        project = hq_models.Project.objects.get(pk=project_id)
        labor_item = LaborItem.objects.get(pk=labor_item_id)
        li_class = LaborClass(pk=li_class_id)

        task = Task.objects.get(pk=task_id)
        
        task.project = project
        task.description = description
        task.started = started
        task.finished = finished
        task.labor_item_number = labor_item
        task.li_class = li_class
        
        task.save()

        return HttpResponseRedirect('/kronos/%s/task/%s' % (timecard_id, task_id))
    else:
        timecard = Timecard.objects.get(pk=timecard_id)
        task = Task.objects.get(pk=task_id)
        li_classes = LaborClass.objects.all()
        labor_groups = LaborGroup.objects.all()
        projects = hq_models.Project.objects.all().filter(archived=False)
        return render(request, 'kronos/task_update.html', {
            'timecard': timecard,
            'task': task,
            'projects': projects,
            'labor_groups': labor_groups,
            'li_classes': li_classes
            })

@login_required(login_url="/login/")
def task_copy(request, timecard_id, task_id):
    """/kronos/1/task/1/delete/
    Copy task with id, replace times with today
    """
    t = Task.objects.get(pk=task_id)
    t.pk = None

    today = datetime.datetime.now()
    
    t.started = t.started.replace(year=today.year, month=today.month, day=today.day)
    t.finished = t.finished.replace(year=today.year, month=today.month, day=today.day)
    t.save()
    return HttpResponseRedirect('/kronos/%s/' % (timecard_id))

@login_required(login_url="/login/")
def task_delete(request, timecard_id, task_id):
    """/kronos/1/task/1/delete/
    Delete the task with id.
    """
    t = Task.objects.get(pk=task_id)
    t.delete()
    return HttpResponseRedirect('/kronos/%s' % (timecard_id))
