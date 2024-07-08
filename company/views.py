from django.shortcuts import render
from company.models import Designation, Employee
from company.forms import EmployeeForm, DesignationForm
from django.contrib import messages #import messages
from django.utils.translation import gettext_lazy as _
from mandoob.models import Mandoob
from mandoob.forms import MandoobForm

from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required()
def designations(request):
    company = request.user.employee.company
    designations = Designation.objects.filter(company = company)
    context = {
        'designations': designations
    }

    return render(request, 'designation_list.html', context)



@login_required()
def add_designation(request):
    form = DesignationForm()
    form.fields['company'].initial = request.user.employee.company.pk
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New Designation has been Created.'))
            return render(request, "close_popup.html")


        else:
            messages.error(request, _('Something went wrong'))
    context = {'form': form}
    return render(request, "forms/designation_form.html", context)


@login_required()
def employees(request):
    company = request.user.employee.company
    employees = Employee.objects.filter(company = company)
    context = {
        'employees': employees
    }
    return render(request, 'employee_list.html', context)

@login_required()
def add_employee(request):
    form = EmployeeForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['designation'].queryset = Designation.objects.filter(company = request.user.employee.company.id)

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New employee has been registered.'))
            return render(request, "close_popup.html")
        context = {'form' : form}
        return render(request, 'forms/employee_form.html', context)
        

        


    context = {'form' : form}
    return render(request, 'forms/employee_form.html', context)



@login_required()
def edit_employee(request, pk):
    company = request.user.employee.company.id
    employee = Employee.objects.get(id = pk, company = company)
    
    if request.method == "GET":
        form = EmployeeForm(instance=employee)
        form.fields['designation'].queryset = Designation.objects.filter(company = request.user.employee.company.id)

        context = {'form': form}
        return render(request, 'forms/employee_form.html', context)
    elif request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, _("Employee record has been updated."))
            return render(request, "close_popup.html")
        else:
            context['form'] = form
            return render(request, 'forms/employee_form.html', context)



        

    return


@login_required()
def mandoobs(request):
    company = request.user.employee.company
    mandoobs = Mandoob.objects.filter(company = company)
    context = {
        'mandoobs': mandoobs
    }

    return render(request, 'mandoob_list.html', context)


def add_mandoob(request):
    form = MandoobForm()
    form.fields['company'].initial = request.user.employee.company.pk
    if request.method == 'POST':
        form = MandoobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New Mandoob has been Created.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Something went wrong'))
    context = {'form': form,
               'title': _('Add Mandoob')}

    return render(request, "form.html", context)

def edit_mandoob(request, pk):
    company = request.user.employee.company.id
    mandoob = Mandoob.objects.get(id = pk, company = company)
    
    if request.method == "GET":
        form = MandoobForm(instance=mandoob)
        context = {'form': form}
        return render(request, 'form.html', context)
    elif request.method == "POST":
        form = MandoobForm(request.POST, instance=mandoob)
        if form.is_valid():
            form.save()
            messages.success(request, _("Mandoob record has been updated."))
            return render(request, "close_popup.html")
        else:
            context['form'] = form
            context['title'] = _('Edit Mandoob')
            return render(request, 'form.html', context)



