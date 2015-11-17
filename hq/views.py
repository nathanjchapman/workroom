from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Address, Project
from .forms import AddressForm, ProjectForm

def overview(request):
    p = Project.objects.all().filter(archived=False)
    a = Address.objects.all()
    return render(request, 'hq/overview.html', {
        'projects': p,
        'addresses': a
        })

# /hq/project/add/
def project_add(request):
    # if POST process data and create project
    if request.method == "POST":

        f = ProjectForm(request.POST)

        new_project = f.save()

        new_project.save()

        return HttpResponseRedirect('/hq/project/%s' % (new_project.id))

    else:
        form = ProjectForm()
        return render(request, 'hq/project_add.html', {'form': form.as_p()})

# /hq/address/add/
def address_add(request):
    # if POST process data and create address
    if request.method == "POST":


        f = AddressForm(request.POST)

        new_address = f.save()

        new_address.save()

        return HttpResponseRedirect('/hq/address/%s' % (new_address.id))

    else:
        form = AddressForm()
        return render(request, 'hq/address_add.html', {'form': form.as_p()})

def project_detail(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist.")
    return render(request, 'hq/project_detail.html', {
        'project': project
        })

def address_detail(request, address_id):
    try:
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        raise Http404("Address does not exist.")
    return render(request, 'hq/address_detail.html', {
        'address': address
        })

# /hq/1/project/1/delete/
# delete the project with id
def project_delete(request, project_id):
    p = Project.objects.get(pk=project_id)
    p.delete()
    return HttpResponseRedirect('/hq/')

def project_archive(request, project_id):
    p = Project.objects.get(pk=project_id)
    p.archived = True
    p.save()
    return HttpResponseRedirect('/hq/')

# /hq/1/address/1/delete/
# delete the address with id
def address_delete(request, address_id):
    a = Address.objects.get(pk=address_id)
    a.delete()
    return HttpResponseRedirect('/hq/')