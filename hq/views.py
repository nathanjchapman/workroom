from django.shortcuts import render
from .models import Address, Project
from .forms import ProjectForm

# /hq/project/add/
def project_add(request):
    # if POST process data and create project
    if request.method == "POST":

        p = Project.objects.create(request.POST)
        p.save()

        return HttpResponseRedirect('/hq/')

    else:
        form = ProjectForm()
        return render(request, 'hq/project_add.html', {'form': form})

# /hq/address/add/
def address_add(request):
    # if POST process data and create address
    if request.method == "POST":


        tc = Project.objects.create(
            )
        tc.save()

        return HttpResponseRedirect('/hq/')

    else:
        return render(request, 'hq/address_add.html')