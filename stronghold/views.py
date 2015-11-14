from django.shortcuts import render
from .models import Door, Code
from .forms import CodeForm

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
    pass

def code_add(request):
    f = CodeForm()
    return render(request, 'stronghold/code_add.html', {'form': f.as_p()})

def code_detail():
    pass