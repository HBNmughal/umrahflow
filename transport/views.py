from django.shortcuts import render
from .models import TransportRoute, TransportCompany, TransportPackage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import TransportRouteForm, TransportCompanyForm, TransportPackageForm
from django.shortcuts import get_object_or_404
from .tables import TransportRouteTable, TransportPackageTable
from django_tables2 import RequestConfig
# login required
from django.contrib.auth.decorators import login_required
# Create your views here.


# trabsport routes list of the company
@login_required
def transport_routes(request):
    transport_routes = TransportRoute.objects.filter(company=request.user.employee.company).order_by('-id')
    table = TransportRouteTable(transport_routes)
    
    # Using RequestConfig to configure pagination and other options
    RequestConfig(request, paginate={"per_page": 5}).configure(table)
    
    context = {
        'table': table,
        'routes': transport_routes,
    }
    return render(request, 'transport_routes.html', context)
# add transport route
@login_required()
def add_transport_route(request):
    if request.method == 'POST':
        add_route_form = TransportRouteForm(request.POST)
        if add_route_form.is_valid():
            route = add_route_form.save(commit=False)
            route.company = request.user.employee.company
            route.save()
            messages.success(request, _('Transport route added successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error adding transport route'))
            return render(request, 'close_popup.html')
    else:
        add_route_form = TransportRouteForm()
        context = {
            'form': add_route_form,
        }
        return render(request, 'add_transport_route.html', context)
    

@login_required()
def transport_schedule_list(request):
    context = {}
    return render(request, 'transport_schedule.html', context)


@login_required()
def edit_transport_route(request, route_id):
    route = get_object_or_404(TransportRoute, id=route_id, company=request.user.employee.company)
    if request.method == 'POST':
        edit_route_form = TransportRouteForm(request.POST, instance=route)
        if edit_route_form.is_valid():
            edit_route_form.save()
            messages.success(request, _('Transport route edited successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error editing transport route'))
            return render(request, 'close_popup.html')
    else:
        edit_route_form = TransportRouteForm(instance=route)
        context = {
            'form': edit_route_form,
        }
        return render(request, 'add_transport_route.html', context)
    
@login_required()
def transport_company_add(request):
    form = TransportCompanyForm()
    if request.method == 'POST':
        form = TransportCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Transport company added successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error adding transport company'))
            return HttpResponseRedirect(reverse('transport_company_form'))
    else:
        form.fields['company'].initial = request.user.employee.company
        context = {
            'title': _('Add Transport Company'),
            'form': form,
        }
        return render(request, 'form.html', context)

@login_required()
def edit_transport_company(request, pk):
    company = get_object_or_404(TransportCompany, id=pk)
    form = TransportCompanyForm(instance=company)
    if request.method == 'POST':
        form = TransportCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, _('Transport company edited successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error editing transport company'))
            return HttpResponseRedirect(reverse('edit_transport_company', kwargs={'pk': pk}))
    else:
        context = {
            'title': _('Edit Transport Company'),
            'form': form,
        }
        return render(request, 'form.html', context)
    

@login_required()
def transport_package_list(request):
    package_list = TransportPackage.objects.filter(company=request.user.employee.company).order_by('-id')
    table = TransportPackageTable(package_list)
    context = {
        'packages': package_list,
        'table': table,
    }
    return render(request, 'transport_packages.html', context)

@login_required()
def transport_package_form(request, pk=None):
    if pk:
        package = get_object_or_404(TransportPackage, id=pk, company=request.user.employee.company)
    else:
        package = TransportPackage(company=request.user.employee.company)
    form = TransportPackageForm(instance=package)
    if request.method == 'POST':
        form = TransportPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, _('Transport package added successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error adding transport package'))
            return HttpResponseRedirect(reverse('transport_package_form'))
    else:
        context = {
            'title': _('Add Transport Package'),
            'form': form,
        }
        return render(request, 'form.html', context)