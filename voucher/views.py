from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import AgentVoucher, FixedVoucherPrices, TransportInvoice
from .forms import AgentVoucherForm, TransportInvoiceForm
from agent.models import Agent, Agent
from django.core.exceptions import ObjectDoesNotExist
from company.models import Company 
from django.contrib import messages #import messages
from django.utils.translation import gettext_lazy as _
from payment.models import AgentPaymentTransaction
from django.contrib.auth.decorators import login_required, permission_required
from .filters import AgentVoucherFilter, TransportInvoiceFilter
from django.db.models import Avg, Count, Min, Sum, ExpressionWrapper, DecimalField,F
from arrival_voucher.models import ArrivalVoucher
import datetime

# Create your views here.



@login_required()
def sub_agent_voucher_list(request):
    initial_prices = FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    company = request.user.employee.company
    # vouchers = AgentVoucher.objects.filter(company=company)
    # myFilter = AgentVoucherFilter(request.GET, queryset=vouchers)
    agents = Agent.objects.filter(company=request.user.employee.company)
    # vouchers = myFilter.qs

    context = {
        # 'myFilter': myFilter,
        # "vouchers": vouchers,
        "initial_prices" : initial_prices,
        "agents": agents,
        "custom_datatable_script": True,

    }
    return render(request, "voucher_list/sub_agent_voucher_list.html", context)


@permission_required('voucher.can_add_visa_invoice')
def add_new_voucher(request, type):
    initial_price =  FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    form = AgentVoucherForm()
    agents = Agent.objects.filter(company=request.user.employee.company)
    if request.method == 'POST':
        voucher = AgentVoucher()
        voucher.company = request.user.employee.company
        voucher.agent = Agent.objects.get(id=int(request.POST.get('agent'))) 
        voucher.voucher_no = request.POST.get('voucher_no')
        voucher_alread_exist = AgentVoucher.objects.filter(company = request.user.employee.company.id, voucher_no = voucher.voucher_no)
        if voucher_alread_exist:
            messages.error(request, _("Voucher number already exist."))
            return render(request, "popup_forms/add_voucher.html", {'form': form, "initial_prices" : initial_price, 'agents': agents})
        else:
            pass
        voucher.pax = request.POST.get('pax') 
        voucher.date = request.POST.get('date') 
        voucher.group_no = request.POST.get('group_no') 
        voucher.extra_fees = request.POST.get('additional_services_price')
        voucher.ground_services_price = request.POST.get('ground_services_price') 
        voucher.processing_fees = request.POST.get('processing_fees') 
        voucher.visa_fees = request.POST.get('visa_fees')
        voucher.insurance_price = request.POST.get('insurance_price') 
        voucher.transport_brn_price = request.POST.get('transport_brn_price') 
        voucher.makkah_brn_price = request.POST.get('makkah_brn_price')
        voucher.medina_brn_price =  request.POST.get('medina_brn_price')
        voucher.sale_price = request.POST.get('sale_price')
        voucher.transport_brn_return = request.POST.get('transport_brn_return') 
        voucher.makkah_brn_return = request.POST.get('makkah_brn_return') 
        voucher.medina_brn_return = request.POST.get('medina_brn_return') 
        voucher.vat_return = 15.00
        voucher.ground_services_price_return = 100.00
        voucher.amount = request.POST.get('amount') or 0.00
        voucher.commission = request.POST.get('commission') or 0.00
        voucher.agent_return = request.POST.get('agent_return') or 0.00
        voucher.save()
    
        messages.success(request, _("Voucher added successfully."))
        return render(request, 'close_popup.html')
    date = datetime.date.today()
    context = {'form': form,
    "initial_prices" : initial_price,
    'agents': agents,
    'date': date
    }
    return render(request, "popup_forms/add_voucher.html", context)

def multiply_fees(ground_services_price, additional_services_price, processing_fees,visa_fees,insurance_price, pax):
    ground_services_price = ground_services_price * pax
    additional_services_price = additional_services_price * pax
    processing_fees = processing_fees * pax
    visa_fees = visa_fees * pax
    insurance_price = insurance_price * pax
    context = {
        "ground_services_price": ground_services_price,
        "additional_services_price": additional_services_price,
        "processing_fees": processing_fees,
        "visa_fees": visa_fees,
        "insurance_price": insurance_price,
    }
    return context

@permission_required('voucher.can_edit_visa_invoice')
def edit_voucher(request, type, voucher_id):
    initial_price =  FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    basic_fees = FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    voucher = AgentVoucher.objects.get(company = request.user.employee.company.id, id=voucher_id)
    agents = Agent.objects.filter(company=request.user.employee.company)

    _basic_fees = multiply_fees(basic_fees.ground_services_price, basic_fees.additional_services_price, basic_fees.processing_fees,basic_fees.visa_fees,basic_fees.insurance_price, voucher.pax)
    if request.method == 'POST':
        voucher.date = request.POST.get('date')
        voucher.group_no = request.POST.get('group_no')
        voucher.voucher_no = request.POST.get('voucher_no')
        voucher.agent = Agent.objects.get(id=int(request.POST.get('agent')))
        voucher.ground_services_price = _basic_fees['ground_services_price']
        voucher.additional_services_price =  _basic_fees['additional_services_price']
        voucher.processing_fees =   _basic_fees['processing_fees']
        voucher.visa_fees =  _basic_fees['visa_fees']
        voucher.insurance_price =  _basic_fees['insurance_price']
        voucher.transport_brn_price = request.POST.get('transport_brn_price')
        voucher.makkah_brn_price = request.POST.get('makkah_brn_price')
        voucher.medina_brn_price =  request.POST.get('medina_brn_price')
        voucher.sale_price = request.POST.get('sale_price')
        voucher.transport_brn_return = request.POST.get('transport_brn_return')
        voucher.makkah_brn_return = request.POST.get('makkah_brn_return')
        voucher.medina_brn_return = request.POST.get('medina_brn_return')
        voucher.amount = request.POST.get('amount')
        voucher.vat_return = 15.00
        voucher.ground_services_price_return = 100.00
        voucher.commission = request.POST.get('commission') or 0.00
        voucher.agent_return = request.POST.get('agent_return') or 0.00
        voucher.pax = request.POST.get('pax')

        
        voucher.save()
        messages.success(request, _('Voucher Detailes Updated'))
        return render(request, "close_popup.html")
    context = {
        "voucher":voucher,
        "basic_fees": _basic_fees,
        'initial_prices' : initial_price,
        'agents': agents
        }
    return render(request, 'popup_forms/add_voucher.html', context)

@login_required()
def initial_voucher_price(request):
    initial_prices = FixedVoucherPrices.objects.get(company = request.user.employee.company.id)
    if request.method == "POST":
        initial_prices.ground_services_price = request.POST.get('ground_services_price')
        initial_prices.additional_services_price  = request.POST.get('additional_services_price')
        initial_prices.processing_fees  = request.POST.get('processing_fees')
        initial_prices.insurance_price   = request.POST.get('insurance_price')
        initial_prices.transport_brn_price   = request.POST.get('transport_brn_price')
        initial_prices.makkah_brn_price = request.POST.get('makkah_brn_price')
        initial_prices.medina_brn_price  = request.POST.get('medina_brn_price')
        initial_prices.transport_brn_return  = request.POST.get('transport_brn_return')
        initial_prices.makkah_brn_return  = request.POST.get('makkah_brn_return')
        initial_prices.medina_brn_return = request.POST.get('medina_brn_return')
        initial_prices.save()
        messages.success(request, _("Initial prices saved successfully."))
        return HttpResponseRedirect(reverse('sub_agent_voucher_list'))
    context = {
        "initial_prices" : initial_prices
    }
    return HttpResponseRedirect(reverse('sub_agent_voucher_list'))

def print_voucher(request ,type, voucher_id):
    
    voucher = AgentVoucher.objects.get(company = request.user.employee.company.id, id=voucher_id)
    
    context = {
        'voucher' : voucher
    }
    return render(request, 'print/print_detailed_voucher.html', context)

@login_required()
def print_voucher_list(request, agent_type):
    company = request.user.employee.company
    
    vouchers = AgentVoucher.objects.filter(company=company)
    myFilter = AgentVoucherFilter(request.GET, queryset=vouchers)
    vouchers = myFilter.qs.order_by('date')
    if request.GET.get('agent') and request.GET.get('agent') != None:
        agent = Agent.objects.get(id = request.GET.get('agent'))
    else:
        print("Agent not found")
        agent = _("All Agents")

    total_profit = 0.00
    total_returns = 0.00
    total_vat = 0.00
    total_commission = 0.00
    total_sales = 0.00


    for voucher in vouchers:
        v = voucher.voucher_total()
        total_profit += float(v['profit'])
        total_returns += float(v['returns'])
        total_vat += float(v['vat_return'])
        total_sales += float(v['sale_price'])
        total_commission += float(v['commission'])


    totals = myFilter.qs.aggregate(
        pax=Sum('pax'),
        cost=Sum('amount'),
        sale=Sum('sale_price'),
        
        )
    

    context = {
        'myFilter': myFilter,
        "vouchers": vouchers,
        'total': totals,
        'total_profit': total_profit,
        'total_vat': total_vat,
        'total_returns': total_returns,
        'total_commission': total_commission,
        'total_sales': total_sales,
        "current_agent": agent


        

    }
    return render(request, "print/vouchers_report.html", context)

@login_required()
def delete_voucher(request):
    if request.method == 'POST':
        voucher = request.POST.get('voucher')
        voucher_record = AgentVoucher.objects.get(id=voucher)
        voucher_record.delete()
        messages.success(request, _("Voucher has been deleted successfully."))
        return render(request, 'close_popup.html') 
    
@login_required()
def transport_invoice_list(request):
    company = request.user.employee.company
    invoices = TransportInvoice.objects.filter(company=company)
    agents = Agent.objects.filter(company=request.user.employee.company)
    myFilter = TransportInvoiceFilter(request.GET, queryset=invoices)
    invoices = myFilter.qs.order_by('date')
    context = {
        'myFilter': myFilter,
        "invoices": invoices,
        'agents': agents
    }
    return render(request, "transport_invoice_list.html", context)

@login_required()
def add_transport_invoice(request):
    print("Transport Invoice Form")
    agents = Agent.objects.filter(company=request.user.employee.company)
    form = TransportInvoiceForm()
    form.fields['agent'].queryset = agents
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['arrival_voucher'].queryset = ArrivalVoucher.objects.filter(company=request.user.employee.company)


    if request.method == "POST":
        form = TransportInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = request.user.employee.company
            invoice.save()
            messages.success(request, _("Invoice has been added successfully.") + _("Invoice No.")+ " " +str(invoice.id))
            return render(request, 'close_popup.html') 
    context = {
        'form': form,
        'agents': agents
    }   
    return render(request, 'transport_invoice_form.html', context)

def edit_transport_invoice(request, invoice_id):
    invoice = TransportInvoice.objects.get(id=invoice_id)
    agents = Agent.objects.filter(company=request.user.employee.company)
    form = TransportInvoiceForm(instance=invoice)

    form.fields['agent'].queryset = agents
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['arrival_voucher'].queryset = ArrivalVoucher.objects.filter(company=request.user.employee.company)


    if request.method == "POST":
        form = TransportInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = request.user.employee.company
            invoice.save()
            messages.success(request, _("Invoice has been updated successfully.") + _("Invoice No.")+ " " +str(invoice.id))
            return render(request, 'close_popup.html') 
    context = {
        'form': form,
        'agents': agents,
        'invoice': invoice,
    }   
    return render(request, 'transport_invoice_form.html', context)

@login_required()
def delete_transport_invoice(request):
    if request.method == 'POST':
        invoice = request.POST.get('invoice')
        invoice_record = TransportInvoice.objects.get(id=invoice)
        invoice_record.delete()
        messages.success(request, _("Invoice has been deleted successfully.")+ _("Invoice No.")+ " " +str(invoice))
        return render(request, 'close_popup.html')

    else:
        return render(request, 'close_popup.html')
