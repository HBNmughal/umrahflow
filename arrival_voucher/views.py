from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (ArrivalVoucherGroupDetailsForm, 
                    ArrivalVoucherFlightDetailsForm, ArrivalVoucherAccommodationDetailsForm, GroupLeaderForm, TransportBrnForm, RawdahPermitForm, ArrivalVoucherForm, ArrivalVoucherApprovalForm,
                    OperatingScheduleFilterForm, ArrivalVoucherFilterForm
                    )
from django.contrib import messages 
from django.utils.translation import gettext_lazy as _
from transport.models import TransportRoute, TransportMovement, TransportType, TransportCompany
from transport.forms import TransportMovementForm, TransportMovementFormset, MovementDriverForm, MovementStatusForm
from django.contrib.auth.decorators import login_required
from agent.models import Agent
import datetime
from .filters import OperatingScheduleFilter
from company.models import Company
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.db.models import Q
from .models import ArrivalVoucher
from django.forms import forms



@login_required()
def arrival_voucher_list(request):
    add_voucher_form = ArrivalVoucherGroupDetailsForm()
    add_voucher_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)

    # get all arrival vouchers for the company order by date
    arrival_vouchers = ArrivalVoucher.objects.filter(company=request.user.employee.company).order_by('-id')
    add_voucher_form.fields['company'].initial = request.user.employee.company
    arrival_voucher_filter_form = ArrivalVoucherFilterForm(request.GET or None)
    context = {
        'arrival_vouchers': arrival_vouchers,
        'add_voucher_form': add_voucher_form,
        'filter_form': arrival_voucher_filter_form,
    }
    return render(request, 'arrival_voucher_list.html', context)

@login_required()
def add_arrival_voucher(request):
    if request.method == 'POST':
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm(request.POST)
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
        if arrival_voucher_group_details_form.is_valid():
            agent = Agent.objects.get(pk=arrival_voucher_group_details_form.cleaned_data['agent'].pk)
            
            voucher = arrival_voucher_group_details_form.save(commit=False)
            voucher.company = request.user.employee.company
            if arrival_voucher_group_details_form.cleaned_data['pax'] + agent.total_transport_pax() > agent.total_visas():
                messages.warning(request, _('Arrival voucher created successfully with the following warning: Number of pax is greater than the number of visas'))
            else:
                voucher.save()
                messages.success(request, _('Arrival voucher created successfully'))
            voucher.status = 'approved'
            voucher.save()
            return HttpResponseRedirect(reverse_lazy('arrival_voucher', args=[voucher.pk]))
        else:
            messages.error(request, _('Error while creating arrival voucher'))
            context = {
            'form': arrival_voucher_group_details_form,
            }
            return render(request, 'popup_forms/voucher_popup_form.html', context)
    else:
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm()
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
        arrival_voucher_group_details_form
        context = {
            'form': arrival_voucher_group_details_form,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)
    
# @login_required()
# def arrival_voucher(request, pk):
#     voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
#     allow_edit = True
#     if voucher.status == 'pending':
#         allow_edit = False
#     elif voucher.status == 'approved':
#         allow_edit = False
#     elif voucher.status == 'rejected':
#         allow_edit = True

#     allow_edit = True

    
#     group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher)
#     arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher)
#     arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher)
#     transport_brn_form = TransportBrnForm(instance=voucher)
#     for fieldname in group_details_form.fields:
#         group_details_form.fields[fieldname].disabled = True
#     for fieldname in arrival_voucher_flight_details_form.fields:
#         arrival_voucher_flight_details_form.fields[fieldname].disabled = True
#     for fieldname in arrival_voucher_accommodation_details_form.fields:
#         arrival_voucher_accommodation_details_form.fields[fieldname].disabled = True

#     for fieldname in transport_brn_form.fields:
#         transport_brn_form.fields[fieldname].disabled = True
    
#     full_form = ArrivalVoucherForm(instance=voucher)
#     if request.method == 'POST':
#         full_form = ArrivalVoucherForm(request.POST, instance=voucher)
#         if full_form.is_valid():
#             full_form.save()
#             messages.success(request, _('Arrival voucher updated successfully'))
#             return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
#         else:
#             messages.error(request, _('Error updating arrival voucher'))
#             return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))

#     transport_formset = TransportMovementFormset(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk))

#     if allow_edit == False:
#         for form in transport_formset:
#             for fieldname in form.fields:
#                 form.fields[fieldname].disabled = True

#     context = {

#         'group_details_form': group_details_form,
#         'arrival_voucher_flight_details_form': arrival_voucher_flight_details_form,
#         'arrival_voucher_accommodation_details_form': arrival_voucher_accommodation_details_form,
#         'transport_brn_form': transport_brn_form,
#         'full_form': full_form,

#         'voucher': voucher,
#         'transport_formset': transport_formset,
#     }
#     return render(request, 'arrival_voucher_form.html', context)

@login_required()
def arrival_voucher_flight_details_form(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(request.POST, instance=voucher)
        if arrival_voucher_flight_details_form.is_valid():
            arrival_voucher_flight_details_form.save()
            messages.success(request, _('Arrival voucher flight details updated successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error updating arrival voucher flight details'))
            return render(request, 'close_popup.html')
    else:
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher)
        context = {
            'form': arrival_voucher_flight_details_form,
            'voucher': voucher,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)


@login_required()
def arrival_voucher_accommodation_details_form(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(request.POST, instance=voucher)
        if arrival_voucher_accommodation_details_form.is_valid():
            arrival_voucher_accommodation_details_form.save()
            messages.success(request, _('Arrival voucher accommodation details updated successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error updating arrival voucher accommodation details'))
            return render(request, 'close_popup.html')
    else:
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher)
        context = {
            'form': arrival_voucher_accommodation_details_form,
            'voucher': voucher,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)

@login_required()
def arrival_voucher_group_details_form(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm(request.POST, instance=voucher)
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)

        if arrival_voucher_group_details_form.is_valid():
            arrival_voucher_group_details_form.save()
            messages.success(request, _('Arrival voucher group details updated successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error updating arrival voucher group details'))
            return render(request, 'close_popup.html')
    else:
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher)
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
        arrival_voucher_group_details_form
        context = {
            'form': arrival_voucher_group_details_form,
            'voucher': voucher,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)

@login_required()
def transport_brn_form(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        transport_brn_form = TransportBrnForm(request.POST, instance=voucher)
        if transport_brn_form.is_valid():
            transport_brn_form.save()
            messages.success(request, _('Transport BRN updated successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error updating transport BRN'))
            return render(request, 'close_popup.html')
    else:
        transport_brn_form = TransportBrnForm(instance=voucher)
        transport_brn_form.fields['transport_type'].queryset = TransportType.objects.filter(company=request.user.employee.company)
        transport_brn_form.fields['transport_company'].queryset = TransportCompany.objects.filter(company=request.user.employee.company)

        context = {
            'form': transport_brn_form,
            'voucher': voucher,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)

    

@login_required()
def transport_movement_form(request, voucher_id):
    voucher = ArrivalVoucher.objects.get(pk=voucher_id)
    print(voucher)
    form = TransportMovementForm()
    form.fields['voucher'].initial = voucher_id
    if request.method == 'POST':
        form = TransportMovementForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.company = request.user.employee.company
            form.agent = voucher.agent
            form.voucher = voucher.pk
            form.type = voucher.transportation_type
            form.save()
            messages.success(request, _('Transport movement added successfully'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': voucher_id}))
        else:
            print(form.errors)
            messages.error(request, _('Error adding transport movement'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': voucher_id}))
    else:
        form = TransportMovementForm(instance=voucher)
        context = {
            'form': form,
            'voucher': voucher,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)


@login_required()
def transport_movement_formset(request, voucher_id):
    voucher = ArrivalVoucher.objects.get(pk=voucher_id)
    form = TransportMovementFormset(request.POST or None, instance=voucher)
    full_form = ArrivalVoucherForm(instance=voucher)

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.company = request.user.employee.company
            form.agent = voucher.agent
            form.voucher = voucher.pk
            form.save()
            messages.success(request, _('Transport movement added successfully'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': voucher_id}))
        else:
            messages.error(request, _('Error adding transport movement'))
            form = TransportMovementFormset(instance=voucher)
            context = {
                'form': form,
                'voucher': voucher,
                'full_form': full_form,
                'transport_formset': form,

            }
            return render(request,'arrival_voucher_form.html', context)
            
    else:
        form = TransportMovementFormset(instance=voucher)
        context = {
            'voucher': voucher,
            'full_form': full_form,
            'transport_formset': form,

        }
        return render(request,'arrival_voucher_form.html', context)

@login_required()
def arrival_voucher_submit(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        voucher.status = 'pending'
        voucher.save()
        messages.success(request, _('Arrival voucher submitted for approval successfully'))
        return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
    else:
        messages.error(request, _('Error submitting arrival voucher for approval'))
        return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
    

@login_required()
def arrival_vouchers_waiting_approval(request):
    vouchers = ArrivalVoucher.objects.filter(status='pending')
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'arrival_vouchers_waiting_approval.html', context)

@login_required()
def arrival_voucher_approve(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        voucher.status = 'approved'
        voucher.save()
        messages.success(request, _('Arrival voucher approved successfully'))
        return HttpResponseRedirect(reverse('arrival_vouchers_waiting_approval'))
    else:
        messages.error(request, _('Error approving arrival voucher'))
        return HttpResponseRedirect(reverse('arrival_vouchers_waiting_approval'))

@login_required()
def arrival_voucher_reject(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        voucher.status = 'rejected'
        voucher.save()
        messages.success(request, _('Arrival voucher rejected successfully'))
        return HttpResponseRedirect(reverse('arrival_vouchers_waiting_approval'))
    else:
        messages.error(request, _('Error rejecting arrival voucher'))
        return HttpResponseRedirect(reverse('arrival_vouchers_waiting_approval'))
    
def arrival_voucher_print(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    transport_movements = TransportMovement.objects.filter(voucher=voucher.pk, outside_package=False).order_by('date', 'time')
    transport_movements_outside_package = TransportMovement.objects.filter(voucher=voucher.pk, outside_package=True).order_by('date', 'time')

    context = {
        'voucher': voucher,
        'transport_movements': transport_movements,
        'transport_movements_outside_package': transport_movements_outside_package,
    }
    return render(request, 'print/transport_program.html', context)




@login_required()
def operating_schedule(request, day):
    date = day
    if day == 'today':
        date = datetime.date.today()
    elif day == 'tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=1)
    elif day == 'yesterday':
        date = datetime.date.today() - datetime.timedelta(days=1)
    elif day == 'after_tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=2)
    
    

    

    
    filter_form = OperatingScheduleFilterForm(request.GET or None)

    
    if request.GET.get('date'):
        date = request.GET.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    movements = TransportMovement.objects.filter(voucher__company=request.user.employee.company, date=date).order_by('date', 'time')
    
    if request.GET.get('type'):
        type = request.GET.get('type')
        movements = TransportMovement.objects.filter(voucher__company=request.user.employee.company, date=date, type=type).order_by('date', 'time')

    status = request.GET.get('status') or None
    if status:
        movements.filter(status=status)
    if request.GET.get('agent'):
        agent = request.GET.get('agent')
        movements = movements.filter(voucher__agent=agent)
    if request.GET.get('transport_company'):
        transport_company = request.GET.get('transport_company')
        movements = movements.filter(transport_company=transport_company)
    if request.GET.get('transport_type'):
        transport_type = request.GET.get('transport_type')
        movements = movements.filter(type=transport_type)
    

    
    movements = movements.filter(voucher__status='approved').exclude(status='date_open')

    # init date in filter_form
    filter_form.fields['date'].initial = date
    # agent query set in filter_form
    filter_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
    # transport company query set in filter_form
    filter_form.fields['transport_company'].queryset = TransportCompany.objects.filter(company=request.user.employee.company)
    # transport type query set in filter_form
    filter_form.fields['transport_type'].queryset = TransportType.objects.filter(company=request.user.employee.company)

    schedule_for = None

    if request.GET.get('schedule_for') and request.GET.get('schedule_for') == 'jeddah_airport':
        movements = movements.filter(
            Q(route__mandoob_mark_as_on_the_way = 'jeddah_airport') |
            Q(route__mandoob_mark_as_completed = 'jeddah_airport')
            )
        
        schedule_for = _('Jeddah Airport')

        
    elif request.GET.get('schedule_for') and request.GET.get('schedule_for') == 'makkah':
        movements = movements.filter(
            Q(route__mandoob_mark_as_on_the_way = 'makkah') |
            Q(route__mandoob_mark_as_completed = 'makkah')
            )
        schedule_for = _('Makkah')
    elif request.GET.get('schedule_for') and request.GET.get('schedule_for') == 'madinah':
        movements = movements.filter(
            Q(route__mandoob_mark_as_on_the_way = 'madinah') |
            Q(route__mandoob_mark_as_completed = 'madinah')
            )
        schedule_for = _('Medina')
    elif request.GET.get('schedule_for') and request.GET.get('schedule_for') == 'medina_airport':
        movements = movements.filter(
            Q(route__mandoob_mark_as_on_the_way = 'medina_airport') |
            Q(route__mandoob_mark_as_completed = 'medina_airport')
            )
        
        schedule_for = _('Medina Airport')
        

    
    


    context = {
        'movements': movements,
        'date': date,
        'day': day,
        'status': status,
        'filter_form': filter_form,
        'schedule_for': schedule_for,
    }

    

    if request.GET.get('print'):
        
        return render(request, 'print/operating_schedule.html', context)
    return render(request, 'operating_schedule.html', context)




@login_required()
def assign_driver(request, movement_id):
    movement = get_object_or_404(TransportMovement, pk=movement_id, voucher__company=request.user.employee.company)
    if request.method == 'POST':
        form = MovementDriverForm(request.POST, instance=movement)
        if form.is_valid():
            form.save()
            messages.success(request, _('Driver assigned successfully'))
            return render(request, 'close_popup.html')
        else:
            print(form.errors)
            messages.error(request, _('Error assigning driver'))
            return render(request, 'close_popup.html')
    else:
        form = MovementDriverForm(instance=movement)
        context = {
            'form': form,
            'movement': movement,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)

@login_required()
def assign_group_leader(request, movement_id):
    movement = get_object_or_404(TransportMovement, pk=movement_id, voucher__company=request.user.employee.company)
    voucher = movement.voucher
    if request.method == 'POST':
        form = GroupLeaderForm(request.POST, instance=voucher)
        if form.is_valid():
            form.save()
            messages.success(request, _('Group leader assigned successfully'))
            return render(request, 'close_popup.html')
        else:
            print(form.errors)
            for field in form:
                print(field.errors)
            messages.error(request, _('Error assigning group leader'))
            return render(request, 'close_popup.html')
    else:
        form = GroupLeaderForm(instance=voucher)

        context = {
            'form': form,
            'movement': movement,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)
    

@login_required()
def status_change(request, movement_id):
    form = MovementStatusForm(request.POST)
    movement = get_object_or_404(TransportMovement, pk=movement_id, voucher__company=request.user.employee.company)
    if request.method == 'POST':
        if form.is_valid():
            movement.status = form.cleaned_data['status']
            movement.remarks = form.cleaned_data['remarks']
            movement.save()
            messages.success(request, _('Status changed successfully'))
            return render(request, 'close_popup.html')
        else:
            print(form.errors)
            messages.error(request, _('Error changing status'))
            return render(request, 'close_popup.html')
    else:
        form = MovementStatusForm(instance=movement)
        context = {
            'form': form,
            'movement': movement,
        }
        return render(request, 'popup_forms/voucher_popup_form.html', context)

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

    

def print_operating_schedule(request, day):
    date = day
    if day == 'today':
        date = datetime.date.today()
    elif day == 'tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=1)
    elif day == 'yesterday':
        date = datetime.date.today() - datetime.timedelta(days=1)
    elif day == 'after_tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=2)
    if request.GET.get('date'):
        date = request.GET.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    
    
    
    movements = TransportMovement.objects.filter(voucher__company=request.user.employee.company, date=date, voucher__status='approved').order_by('date', 'time').exclude(status='date_open')
    
    if request.GET.get('agent'):
        agent = request.GET.get('agent')
        movements = movements.filter(agent=agent)
    if request.GET.get('transport_company'):
        transport_company = request.GET.get('transport_company')
        movements = movements.filter(transport_company=transport_company)
    if request.GET.get('transport_type'):
        transport_type = request.GET.get('transport_type')
        movements = movements.filter(transport_type=transport_type)

    

    context = {
        'movements': movements,
        'date': date,
        'day': day,
    }


    return render(request, 'print/operating_schedule.html', context)


def schedule_tracking_screen(request, company_id, content=None):
    target_date = timezone.now()  # You can replace this with your specific date

    # Calculate the date range
    date_range_start = target_date - timedelta(days=1)
    date_range_end = target_date + timedelta(days=1)


    transport_movements = TransportMovement.objects.filter(voucher__company=company_id, date__range=(date_range_start, date_range_end)).order_by('date', 'time').filter(voucher__status='approved').exclude(status='date_open')
    company = get_object_or_404(Company, pk=company_id)
    context = {
        'movements': transport_movements,
        'company': company,
     
    }
    if content:
        return render(request, 'schedule_tracking_screen_content.html', context)
    else:
        return render(request, 'schedule_tracking_screen.html', context)




def agent_movements_report_by_transport_company(request, transport_company_id):
    transport_company = get_object_or_404(TransportCompany, pk=transport_company_id)
    movements = TransportMovement.objects.filter(voucher__company=request.user.employee.company, transport_company=transport_company_id).order_by('date', 'time')
    context = {
        'movements': movements,
        'transport_company': transport_company,
    }
    return render(request, 'agent_movements_report_by_transport_company.html', context)


def rawdah_permit_list(request):
    rawdah_permits = ArrivalVoucher.objects.filter(
        Q(rawdah_men_request_date__isnull=False) | 
        Q(rawdah_women_request_date__isnull=False) | 
        Q(rawdah_men_reservation_date__isnull=False) |
        Q(rawdah_women_reservation_date__isnull=False)

        ).filter(company=request.user.employee.company).exclude(rawdah_men_status = 'completed', rawdah_women_status='completed').order_by('rawdah_men_request_date', 'rawdah_women_request_date')
    context = {
        'rawdah_permits': rawdah_permits,
    }
    return render(request, 'rawdah_permit_list.html', context)

def add_rawdah_permit(request):


    if request.method == 'POST':
        form = RawdahPermitForm(request.POST)
        form.agent.queryset = Agent.objects.filter(company=request.user.employee.company)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.company = request.user.employee.company
            permit.save()
            messages.success(request, _('Rawdah permit added successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error adding rawdah permit'))
            form.fields['company'].initial = request.user.employee.company

            form = RawdahPermitForm(request.POST)
            context = {
                'form': form,
            }
            return render(request, 'popup_forms/form.html', context)
    else:
        form = RawdahPermitForm()
        form.fields['company'].initial = request.user.employee.company
        context = {
            'form': form,
        }
        return render(request, 'popup_forms/form.html', context)
    

def edit_rawdah_permit(request, pk):
    permit = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        form = RawdahPermitForm(request.POST, instance=permit)

        if form.is_valid():
            permit = form.save(commit=False)
            permit.company = request.user.employee.company
            permit.save()
            messages.success(request, _('Rawdah permit updated successfully'))
            return render(request, 'close_popup.html')
        else:
            messages.error(request, _('Error updating rawdah permit'))
            form.fields['company'].initial = request.user.employee.company

            form = RawdahPermitForm(request.POST)
            form.agent.queryset = Agent.objects.filter(company=request.user.employee.company)

            context = {
                'form': form,
            }
            return render(request, 'popup_forms/form.html', context)
    else:
        form = RawdahPermitForm(instance=permit)

        form.fields['company'].initial = request.user.employee.company
        context = {
            'form': form,
        }
        return render(request, 'popup_forms/form.html', context)
    
@login_required()
def voucher_movement_history(request, voucher_id):
    history = TransportMovement.history.filter(voucher = voucher_id).distinct().order_by('-history_date')
    
    

    context = {
        'history': history,
        }
    return render(request, 'transport_movement_history.html', context)


def arrival_vouchers_list_htmx(request):
    # page = request.GET.get('page', 1)
    
    # queryset = ArrivalVoucher.objects.filter(company=request.user.employee.company).order_by('-id')
    # paginator = Paginator(queryset, 5) 
    # if request.headers.get('HX-Request') == 'true':
    #     data = {
    #         'arrival_vouchers': render_to_string('arrival_voucher_list_htmx_1.html', {'arrival_vouchers': paginator.page(page)})
    #     }
    #     return JsonResponse(data)
    # context = {
    #     'arrival_vouchers': queryset,
    # }
    return render(request, 'arrival_vouchers_list_htmx.html', )

@login_required()
def arrival_voucher(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company)
    group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher)
    arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher)
    arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher)
    transport_brn_form = TransportBrnForm(instance=voucher)
    transport_movement_formset = TransportMovementFormset(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk))
    rawdah_form = RawdahPermitForm(instance=voucher)
    if request.method == "POST":
        group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
        group_details_form = ArrivalVoucherGroupDetailsForm(request.POST, instance=voucher)
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(request.POST, instance=voucher)
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(request.POST, instance=voucher)
        transport_brn_form = TransportBrnForm(request.POST, instance=voucher)
        transport_movement_formset = TransportMovementFormset(request.POST, instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk))
        rawdah_form = RawdahPermitForm(request.POST, instance=voucher)

        if group_details_form.is_valid() and arrival_voucher_flight_details_form.is_valid() and arrival_voucher_accommodation_details_form.is_valid() and transport_brn_form.is_valid() and transport_movement_formset.is_valid() and rawdah_form.is_valid():
            if group_details_form.has_changed():
                group_details_form.save()
            if arrival_voucher_flight_details_form.has_changed():
                arrival_voucher_flight_details_form.save()
            if arrival_voucher_accommodation_details_form.has_changed():
                arrival_voucher_accommodation_details_form.save()
            if transport_brn_form.has_changed():
                transport_brn_form.save()
            if rawdah_form.has_changed():
                rawdah_form.save()
            if transport_movement_formset.has_changed():
                for form in transport_movement_formset:
                    # check if detele
                    if 'DELETE' in form.changed_data:
                        if form.instance.pk:
                            movement = TransportMovement.objects.get(pk=form.instance.pk)
                            movement.delete()
                    else:
                        if form.has_changed():
                            form.save()
                            if 'date' in form.initial:
                                if form.initial['date'] != form.cleaned_data['date']:
                                    movement = TransportMovement.objects.get(pk=form.instance.pk)
                                    movement.status = 'pending'
                                    movement.first_driver_name = ""
                                    movement.first_driver_phone = ""
                                    movement.second_driver_name = ""
                                    movement.second_driver_phone = ""
                                    movement.no_plate = ""
                                    movement.save()

                                
                            
            

            messages.success(request, _('Arrival voucher updated successfully'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
        else:
            allow_edit = True
            group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.employee.company)
            transport_brn_form.fields['transport_type'].queryset = TransportType.objects.filter(company=request.user.employee.company)


            context = {
                'group_details_form': group_details_form,
                'arrival_voucher_flight_details_form': arrival_voucher_flight_details_form,
                'arrival_voucher_accommodation_details_form': arrival_voucher_accommodation_details_form,
                'transport_brn_form': transport_brn_form,
                'transport_formset': transport_movement_formset,
                'voucher': voucher,
                'rawdah_form': rawdah_form,
                'allow_edit': allow_edit
            }
            messages.error(request, _('Error updating arrival voucher'))
            
            return render(request, 'arrival_voucher.html', context)
    else:
        if voucher.status == 'with_agent_rejected' and voucher.rejected_reason:
            messages.error(request, _("Rejection Reason")+ ": " + str(voucher.rejected_reason))
        group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher)
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher)
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher)
        transport_brn_form = TransportBrnForm(instance=voucher)
        rawdah_form = RawdahPermitForm(instance=voucher)
        transport_formset = TransportMovementFormset(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk))
        allow_approval = False
        allow_edit = True
        if voucher.status in ['pending', 'with_agent_rejected', 'rejected', 'with_agent_draft']:
            for fieldname in group_details_form.fields:
                group_details_form.fields[fieldname].disabled = True
            for fieldname in arrival_voucher_flight_details_form.fields:
                arrival_voucher_flight_details_form.fields[fieldname].disabled = True
            for fieldname in arrival_voucher_accommodation_details_form.fields:
                arrival_voucher_accommodation_details_form.fields[fieldname].disabled = True
            for fieldname in transport_brn_form.fields:
                transport_brn_form.fields[fieldname].disabled = True
            for form in transport_movement_formset:
                for fieldname in form.fields:
                    form.fields[fieldname].disabled = True
            for fieldname in rawdah_form.fields:
                rawdah_form.fields[fieldname].disabled = True
            for form in transport_formset:
                for field in form.fields:
                    form.fields[field].disabled = True
            allow_edit = False
        
        # if voucher.status == 'confirmed':
        #     if request.user.has_perm('arrival_voucher.can_add_extra_movement'):
        #         transport_formset.can_delete = False
        #         transport_formset.extra = 0

        #         for form in transport_formset:
        #             form.fields['date']. = True
        #             form.fields['route'].disabled = True
        #             if form.instance.status == 'completed':
        #                 form.fields['status'].disabled = False


        if voucher.status == 'pending':
                allow_approval = True
                allow_edit = False




        if allow_approval:
            arrival_voucher_approve_form = ArrivalVoucherApprovalForm(instance=voucher)
            arrival_voucher_reject_form = ArrivalVoucherApprovalForm(instance=voucher)
            arrival_voucher_approve_form.fields['status'].initial = 'approved'
            arrival_voucher_reject_form.fields['status'].initial = 'with_agent_rejected'
            arrival_voucher_reject_form.fields['rejected_reason'].required = True
            arrival_voucher_reject_form.fields['rejected_reason']
            if voucher.agent.total_transport_pax() + voucher.pax > voucher.agent.total_visas():
                messages.warning(request, _('Arrival voucher is pending approval with the following warning: Number of pax is greater than the number of visas'))
        else:
            arrival_voucher_approve_form = False
            arrival_voucher_reject_form = False
        context = {
            'group_details_form': group_details_form,
            'arrival_voucher_flight_details_form': arrival_voucher_flight_details_form,
            'arrival_voucher_accommodation_details_form': arrival_voucher_accommodation_details_form,
            'transport_brn_form': transport_brn_form,
            'transport_formset': transport_formset,
            'voucher': voucher,
            'rawdah_form': rawdah_form,
            'allow_approval': allow_approval if allow_approval else False,
            'arrival_voucher_approve_form': arrival_voucher_approve_form if allow_approval else False,
            'arrival_voucher_reject_form': arrival_voucher_reject_form if allow_approval else False,
            'allow_edit': allow_edit
        }
        
        return render(request, 'arrival_voucher.html', context)

@login_required()
def voucher_approval_form(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, company=request.user.employee.company, status__in=['pending', 'with_agent_rejected'])
    total_transport_pax = voucher.agent.total_transport_pax()
    total_visas = voucher.agent.total_visas()
    pax = voucher.pax
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'approve':
            voucher.status = 'approved'
            voucher.save()
            if int(total_transport_pax) + int(pax) > total_visas:
                messages.warning(request, _('Arrival voucher approved successfully with the following warning: Number of pax is greater than the number of visas'))
            else:

                messages.success(request, _('Arrival voucher approved successfully'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
        elif status == 'reject':
            voucher.status = 'with_agent_rejected'
            voucher.rejected_reason = request.POST.get('reason')
            voucher.save()
            messages.success(request, _('Arrival voucher rejected successfully'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))
        else:
            print(status)
            messages.error(request, _('Error changing status'))
            return HttpResponseRedirect(reverse('arrival_voucher', kwargs={'pk': pk}))


@login_required()
def trips_date_open(request):
    trips = TransportMovement.objects.filter(voucher__company=request.user.employee.company, status = 'date_open').order_by('date', 'time')
    context = {
        'movements': trips,
    }
    return render(request, 'trips_date_open.html', context)

