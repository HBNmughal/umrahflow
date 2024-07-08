# views.py
from django.shortcuts import render
from arrival_voucher.models import ArrivalVoucher
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from transport.models import TransportMovement
from transport.forms import MovementStatusForm



@login_required()
def pending_arrival_voucher_invoice_list_htmx(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    data = ArrivalVoucher.objects.filter(
        Q(id__icontains=query) |
        Q(agent__name_en__icontains=query) |
        Q(agent__name_ar__icontains=query) |
        Q(agent__country__name_en__icontains=query) |
        Q(agent__country__name_ar__icontains=query) |
        Q(group_name__icontains=query) |
        Q(group_no__icontains=query) |
        Q(transport_type__name_en__icontains=query) |
        Q(transport_type__name_ar__icontains=query) |
        Q(transport_company__name_en__icontains=query) |
        Q(transport_company__name_ar__icontains=query) |
        Q(pax__icontains=query) |
        Q(agent_referance_no__icontains=query), company=request.user.employee.company
    ).order_by('id')

    data = data.filter(status='approved', accounts_status='pending', transport_status="approved")
    
    
    paginator = Paginator(data, 100)  # Show 10 items per page
    page = paginator.get_page(page_number)
    return render(request, 'htmx/pending_arrival_voucher_invoice_list_htmx.html', {'arrival_vouchers': page})


@login_required()
def approved_arrival_voucher_invoice_list_htmx(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    data = ArrivalVoucher.objects.filter(
        Q(id__icontains=query) |
        Q(agent__name_en__icontains=query) |
        Q(agent__name_ar__icontains=query) |
        Q(agent__country__name_en__icontains=query) |
        Q(agent__country__name_ar__icontains=query) |
        Q(group_name__icontains=query) |
        Q(group_no__icontains=query) |
        Q(transport_type__name_en__icontains=query) |
        Q(transport_type__name_ar__icontains=query) |
        Q(transport_company__name_en__icontains=query) |
        Q(transport_company__name_ar__icontains=query) |
        Q(pax__icontains=query) |
        Q(agent_referance_no__icontains=query), company=request.user.employee.company
    ).order_by('id')

    data = data.filter(status='approved', accounts_status='approved')

    
    
    paginator = Paginator(data, 100)  # Show 10 items per page
    page = paginator.get_page(page_number)
    return render(request, 'htmx/approved_arrival_voucher_invoice_list_htmx.html', {'arrival_vouchers': page})

