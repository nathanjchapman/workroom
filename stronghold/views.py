from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Door, Code
from .forms import DoorForm, CodeForm

def overview(request):
    all_codes = Code.objects.all()
    perm_codes = all_codes.filter(permanent=True)
    tmp_codes = all_codes.filter(permanent=False)

    return render(request, 'stronghold/overview.html', {
        'perm_codes': perm_codes,
        'tmp_codes': tmp_codes
        })

def door_index(request):
    pass

def code_index(request):
    pass

def door_add(request):
    if request.method == "POST":
        f = DoorForm(request.POST)
        new_door = f.save()
        new_door.save()

        return HttpResponseRedirect('/stronghold/')
    else:
        f = DoorForm()
        return render(request, 'stronghold/door_add.html', {'form': f.as_p()})

def code_add(request):
    if request.method == "POST":
        f = CodeForm(request.POST)
        new_code = f.save()
        new_code.save()

        return HttpResponseRedirect('/stronghold/')
    else:
        f = CodeForm()
        return render(request, 'stronghold/code_add.html', {'form': f.as_p()})

def code_detail(request, code_id):
    c = Code.objects.get(pk=code_id)
    return render(request, 'stronghold/code_detail.html', {'code': c})

def code_delete(request, code_id):
    code = Code.objects.get(pk=code_id)
    code.delete()
    return HttpResponseRedirect('/stronghold/')
