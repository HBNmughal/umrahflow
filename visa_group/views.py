from django.shortcuts import render, redirect
from .models import UmrahVisaGroupInvoice, UmrahVisaGroupInvoiceDefaultPrices
from .forms import UmrahVisaGroupInvoiceDefaultPricesForm, UmrahVisaGroupInvoiceForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from agent.models import Agent
# Create your views here.




@login_required()
def umrah_visa_group_invoice_list(request):
    # initial_prices = FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    company = request.user.employee.company
    default_prices_form = UmrahVisaGroupInvoiceDefaultPricesForm(instance=UmrahVisaGroupInvoiceDefaultPrices.objects.get(company=company))
    context = {
        "custom_datatable_script": True,
        "default_prices_form": default_prices_form,

    }
    return render(request, "umrah_visa_group_invoice_list.html", context)




@login_required()
def umrah_visa_group_invoice(request, pk=None):
    company = request.user.employee.company
    if pk:
        invoice = UmrahVisaGroupInvoice.objects.get(pk=pk)
        form = UmrahVisaGroupInvoiceForm(instance=invoice)
        form.fields['agent'].queryset = Agent.objects.filter(company=company, agent_type=invoice.agent.agent_type)
        if request.method == 'POST':
            form = UmrahVisaGroupInvoiceForm(request.POST, instance=invoice)
            if form.is_valid():
                form.save()
                messages.success(request, _('Invoice updated successfully'))
                return redirect('umrah_visa_group_invoice_list')
            else:
                messages.error(request, _('Please correct the errors below'))
    else:
        form = UmrahVisaGroupInvoiceForm(initial={'company': company})
        form.fields['agent'].queryset = Agent.objects.filter(company=company)
    if request.method == 'POST':
        form = UmrahVisaGroupInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company
            invoice.save()
            messages.success(request, _('Invoice saved successfully'))
            return redirect('umrah_visa_group_invoice_list')
        else:
            messages.error(request, _('Please correct the errors below'))
    context = {
        "form": form,
    }
    return render(request, "umrah_visa_group_invoice_form.html", context)










@login_required()
def umrah_visa_group_invoice_default_prices(request):
    company = request.user.employee.company
    default_prices = UmrahVisaGroupInvoiceDefaultPrices.objects.get(company=company)
    form = UmrahVisaGroupInvoiceDefaultPricesForm(instance=default_prices)
    if request.method == 'POST':
        form = UmrahVisaGroupInvoiceDefaultPricesForm(request.POST, instance=default_prices)
        if form.is_valid():
            form.save()
            messages.success(request, _('Default prices updated successfully'))
    context = {
        "form": form,
    }
    return redirect('umrah_visa_group_invoice_list')



