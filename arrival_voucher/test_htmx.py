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
def search_view(request):
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
    ).order_by('-id')
    
    if request.GET.get('status'):
        if request.GET.get('status') == 'all':
            pass
        elif request.GET.get('status') == 'pending':
            data = data.filter(status='pending')
        elif request.GET.get('status') == 'approved':
            approved = ['approved']
            data = data.filter(status__in=approved)
        elif request.GET.get('status') == 'rejected':
            data = data.filter(status__in=['with_agent_rejected', 'rejected'])
    paginator = Paginator(data, 100)  # Show 10 items per page
    page = paginator.get_page(page_number)
    return render(request, 'htmx/arrival_vouchers_search_results.html', {'arrival_vouchers': page})



@login_required()
def status_change_table(request, movement_id):
    form = MovementStatusForm(request.POST)
    movement = get_object_or_404(TransportMovement, pk=movement_id, voucher__company=request.user.employee.company)
    return_path = request.GET.get('return_path')
    
    if request.method == 'POST':
        if form.is_valid():
            movement.status = form.cleaned_data['status']
            movement.save()
            messages.success(request, _('Status changed successfully'))
            return HttpResponseRedirect(return_path)
        else:
            print(form.errors)
            messages.error(request, _('Error changing status'))
            return HttpResponseRedirect(return_path)


