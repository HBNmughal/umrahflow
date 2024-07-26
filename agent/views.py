from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Agent,  AgentPrice, AgentCode, AgentCommission
from .forms import AgentForm, AgentForm, AgentPriceForm, AgentCodeFormset, AgentCommissionForm
from django.contrib import messages #import messages
from django.utils.translation import gettext_lazy as _
from payment.models import AgentPaymentTransaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime
from transport.models import TransportMovement
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from arrival_voucher.models import ArrivalVoucher
from arrival_voucher.forms import ArrivalVoucherGroupDetailsForm, ArrivalVoucherFlightDetailsForm, ArrivalVoucherAccommodationDetailsForm, TransportBrnForm, ArrivalVoucherForm
from transport.forms import TransportMovementFormsetAgent
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django import forms
from transport.models import TransportMovement, TransportType


from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import JsonResponse



@login_required()
def get_agent_price(request):
    agent = request.GET.get('agent')
    transport_included = request.GET.get('transport_included')
    transport_included = True if transport_included == 'true' else False
    response = {}
    agent = Agent.objects.get(id=agent,company = request.user.employee.company)
    if transport_included:
        response = {
            'price': agent.current_visa_including_transport_price()
        } 

    else:
        price = agent.current_visa_price()
        print(price)
        response = {
            'price': price,
        }
    


    
    return JsonResponse(response)






@login_required()
def agent_list(request):
    company = request.user.employee.company
    agents = Agent.objects.filter(company = company)
    sub_agents = Agent.objects.filter(company = company)
    context = {
        "agents": agents,
        "sub_agents": sub_agents

    }
    return render(request, "agent_list.html", context)


@login_required()
def add_agent(request):
    form = AgentForm()
    form.fields['company'].initial = request.user.employee.company.pk
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New Agent Added.'))
            return render(request, "close_popup.html")


        else:
            messages.error(request, _('Something went wrong'))
    context = {'form': form}
    return render(request, "popup_forms/add_agent_popup.html", context)
@login_required()
def add_agent_external(request):
    form = AgentForm()
    form.fields['company'].initial = request.user.employee.company.pk
    form.fields['external_agent'].queryset = Agent.objects.filter(company=request.user.employee.company)   
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New Agent Added.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Something went wrong'))
    context = {'form': form}
    return render(request, "popup_forms/add_agent_popup.html", context)


@login_required()
def edit_agent(request, pk):
    agent = Agent.objects.get(pk=pk)
    form = AgentForm(instance=agent)

    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, _('Agent Updated.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Something went wrong'))
    context = {'form': form}
    return render(request, "popup_forms/edit_agent_popup.html", context)


@login_required()
def agent_price_list(request, pk):

    agent = Agent.objects.get(pk=pk, company=request.user.employee.company)
    prices = AgentPrice.objects.filter(agent=agent).order_by('-date', '-pk')
    form = AgentPriceForm()
    
    form.fields['agent'].initial = agent.pk
    current_price_id = 0
    try:
        p = AgentPrice.objects.filter(agent=agent).latest('date', 'pk')
        current_price_id =  p.pk
    except:
        pass
    
    if request.method == 'POST':
        form = AgentPriceForm(request.POST)
        if form.is_valid():
            form.save()
            changed_by = AgentPrice.objects.get(pk=form.instance.pk)
            changed_by.changed_by = request.user
            changed_by.save()
            
            messages.success(request, _('New Price Added.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Something went wrong'))
    print(current_price_id)
    context = {
        "history": prices,
        "agent": agent,
        "form": form,
        "current_price_id": current_price_id,
    }
    return render(request, "popup_forms/agent_price.html", context)



def create_agent_user(request, pk):
    agent = Agent.objects.get(pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        active = request.POST.get('active')
        if active == 'on':
            active = True
        else:
            active = False
        try:
            user = User.objects.create_user(username=username, password=password)
            user.is_active = active
            user.save()
            agent.user = user
            agent.save()
            messages.success(request, _('New Agent User Added.'))
            return render(request, "close_popup.html")
        except Exception as e:
            messages.error(request, _('Something went wrong: ') + str(e))
    context = {'agent': agent}
    return render(request, "popup_forms/agent_user.html", context)


def edit_agent_user(request, pk):
    agent = Agent.objects.get(pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        password = request.POST.get('password')
        active = request.POST.get('active')
        if active == 'on':
            active = True
        else:
            active = False
        try:
            user = User.objects.get(pk=agent.user.pk)
            if password != '':
                user.set_password(password)
            user.is_active = active
            user.save()
            agent.save()

            messages.success(request, _('Agent User Updated.'))
            return render(request, "close_popup.html")
        except Exception as e:
            messages.error(request, _('Something went wrong: ') + str(e))
    context = {'agent': agent}
    return render(request, "popup_forms/agent_user.html", context)



def reset_agent_user_password(request, pk):
    agent = Agent.objects.get(pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        password = request.POST.get('password')
        try:
            user = User.objects.get(pk=agent.user.pk)
            user.set_password(password)
            user.save()
            agent.save()

            messages.success(request, _('Agent User Updated.'))
            return render(request, "close_popup.html")
        except Exception as e:
            messages.error(request, _('Something went wrong: ') + str(e))
    context = {'agent': agent}
    return render(request, "popup_forms/agent_user.html", context)



def agent_dashboard(request):
    agent = Agent.objects.get(id=request.user.agent.id)
    context = {'agent': agent}
    return render(request, "agent_dashboard.html", context)



def arrival_vouchers_list_htmx(request):
    add_voucher_form = ArrivalVoucherGroupDetailsForm(user=request.user)

    # get all arrival vouchers for the company order by date
    arrival_vouchers = ArrivalVoucher.objects.filter(agent=request.user.agent).order_by('-id')
    add_voucher_form.fields['company'].initial = request.user.agent.company
    page = request.GET.get('page', 1)
    queryset = ArrivalVoucher.objects.filter(agent=request.user.agent).order_by('-id')
    paginator = Paginator(queryset, 5) 
    if request.headers.get('HX-Request') == 'true':
        data = {
            'arrival_vouchers': render_to_string('arrival_voucher_list_htmx_1.html', {'arrival_vouchers': paginator.page(page)})
        }
        return JsonResponse(data)
    context = {
        'arrival_vouchers': queryset,
        'arrival_vouchers': arrival_vouchers,
        'add_voucher_form': add_voucher_form,
    }
    return render(request, 'agent_arrival_vouchers_list_htmx.html', context)

def agent_arrival_voucher_add(request):
    
    agent = Agent.objects.get(id=request.user.agent.id)
    context = {'agent': agent}
    return render(request, "agent_arrival_voucher_add.html", context)



@login_required()
def agent_operating_schedule(request, day):
    date = day
    if day == 'today':
        date = datetime.date.today()
    elif day == 'tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=1)
    elif day == 'yesterday':
        date = datetime.date.today() - datetime.timedelta(days=1)
    elif day == 'after_tomorrow':
        date = datetime.date.today() + datetime.timedelta(days=2)
    elif day == 'all':
        date = None

    else:
        date = day
    

 
    if day == 'all':
        movements = TransportMovement.objects.filter(voucher__agent = request.user.agent ).order_by('date', 'time')
    else:
        movements = TransportMovement.objects.filter(voucher__agent = request.user.agent, date=date).order_by('date', 'time')
    
    if request.GET.get('type'):
        type = request.GET.get('type')
        movements = TransportMovement.objects.filter(voucher__agent = request.user.agent, date=date, type=type).order_by('date', 'time')

    movements = movements.filter(voucher__status='approved')
    context = {
        'movements': movements,
        'date': date,
        'day': day,
    }

    
    return render(request, 'agent_operating_schedule.html', context)



@login_required()
def add_arrival_voucher(request):
    if request.method == 'POST':
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm(request.POST)
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(id=request.user.agent.id)
        max_pax = 51
        total_visas = request.user.agent.total_visas()
        total_transport_pax = request.user.agent.total_transport_pax()
        pax = arrival_voucher_group_details_form.data['pax'] 
        if arrival_voucher_group_details_form.is_valid() and int(pax) <= max_pax:
            voucher = arrival_voucher_group_details_form.save(commit=False)
            voucher.company = request.user.agent.company
            voucher.agent = request.user.agent
            voucher.status = 'with_agent_draft'
            voucher.save()
            if int(total_transport_pax) + int(pax) > total_visas:
                messages.warning(request, _('Arrival voucher has been added successfully, but you have exceeded your transport limit.'))
            else:
                messages.success(request, _('Arrival voucher has been added successfully'))
            return HttpResponseRedirect(reverse_lazy('agent_arrival_voucher', args=[voucher.pk]))
        else:
            messages.error(request, _('Error while creating arrival voucher'))
            if int(pax) > max_pax:
                messages.error(request, _('Max pax limit is 51 per voucher, if you have more than 51 pax, please create another voucher'))
            context = {
            'form': arrival_voucher_group_details_form,
            }

        return HttpResponseRedirect(reverse('agent_arrival_vouchers_list'))
    else:
        arrival_voucher_group_details_form = ArrivalVoucherGroupDetailsForm()
        arrival_voucher_group_details_form.fields['agent'].queryset = Agent.objects.filter(company=request.user.agent)
        arrival_voucher_group_details_form.fields['company'].initial = request.user.agent.company
        arrival_voucher_group_details_form.fields['agent'].initial = request.user.agent
        context = {
            'form': arrival_voucher_group_details_form,
        }
        return HttpResponseRedirect(reverse('agent_arrival_vouchers_list'))
    





@login_required()
def agent_arrival_voucher(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, agent=request.user.agent)
    group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher, user=request.user)
    arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher, user=request.user)
    arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher, user=request.user)
    transport_movement_formset = TransportMovementFormsetAgent(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk))
    if voucher.status == 'pending':
        allow_edit = False
    elif voucher.status == 'approved':
        allow_edit = False
    elif voucher.status == 'with_agent_rejected':
        allow_edit = True
    elif voucher.status == 'with_agent_draft':
        allow_edit = True
    elif voucher.status == 'draft':
        allow_edit = False
    else:
        allow_edit = False

    

    



    if request.method == "POST":
        group_details_form = ArrivalVoucherGroupDetailsForm(request.POST, instance=voucher, user=request.user)
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(request.POST, instance=voucher, user=request.user)
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(request.POST, instance=voucher, user=request.user)
        transport_movement_formset = TransportMovementFormsetAgent(request.POST, instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk), user=request.user)
        max_pax = 51
        pax = group_details_form.data['pax']
        if group_details_form.is_valid() and arrival_voucher_flight_details_form.is_valid() and arrival_voucher_accommodation_details_form.is_valid() and transport_movement_formset.is_valid() and int(pax) <= max_pax:
            group_details_form.save()
            arrival_voucher_flight_details_form.save()
            arrival_voucher_accommodation_details_form.save()
            transport_movement_formset.save()

            messages.success(request, _('Arrival voucher updated successfully'))
            return HttpResponseRedirect(reverse('agent_arrival_voucher', kwargs={'pk': pk}))
        else:
            if int(pax) > max_pax:
                messages.error(request, _('Max pax limit is 51 per voucher, if you have more than 51 pax, please create another voucher'))
            context = {
                'group_details_form': group_details_form,
                'arrival_voucher_flight_details_form': arrival_voucher_flight_details_form,
                'arrival_voucher_accommodation_details_form': arrival_voucher_accommodation_details_form,
                'transport_formset': transport_movement_formset,
                'voucher': voucher,
                'allow_edit': allow_edit,

            }
            return render(request, 'agent_arrival_voucher.html', context)
    else:


        allow_submit = False
        for movement in voucher.transportmovement_set.all():
            if movement:
                allow_submit = True
                break
        
        if voucher.status == 'with_agent_draft' or voucher.status == 'with_agent_rejected':
            for movement in voucher.transportmovement_set.all():
                if movement:
                    allow_submit = True
                    break
            
        else:
            allow_submit = False
            
        


        if voucher.status == 'with_agent_rejected':
            messages.error(request, _(_("Rejection Reason")+ ": " + voucher.rejected_reason))


        group_details_form = ArrivalVoucherGroupDetailsForm(instance=voucher, user=request.user)
        arrival_voucher_flight_details_form = ArrivalVoucherFlightDetailsForm(instance=voucher, user=request.user)
        arrival_voucher_accommodation_details_form = ArrivalVoucherAccommodationDetailsForm(instance=voucher, user=request.user)

        transport_formset = TransportMovementFormsetAgent(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk), user=request.user)

        if allow_edit == False:
            # disable all forms
            for field in group_details_form.fields:
                group_details_form.fields[field].disabled = True
            for field in arrival_voucher_flight_details_form.fields:
                arrival_voucher_flight_details_form.fields[field].disabled = True
            for field in arrival_voucher_accommodation_details_form.fields:
                arrival_voucher_accommodation_details_form.fields[field].disabled = True
            for form in transport_formset:
                for field in form.fields:
                    form.fields[field].disabled = True

        
        context = {
            'group_details_form': group_details_form,
            'arrival_voucher_flight_details_form': arrival_voucher_flight_details_form,
            'arrival_voucher_accommodation_details_form': arrival_voucher_accommodation_details_form,
            'transport_formset': transport_formset,
            'voucher': voucher,
            'allow_edit': allow_edit,
            'allow_submit': allow_submit,

        }
        return render(request, 'agent_arrival_voucher.html', context)
    

@login_required()
def submit_arrival_voucher(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, agent=request.user.agent)
    if voucher.status == 'with_agent_draft' or voucher.status == 'with_agent_rejected':
        voucher.status = 'pending'
        voucher.rejected_reason = ''
        voucher.save()
        messages.success(request, _('Arrival voucher submitted successfully'))
        return HttpResponseRedirect(reverse('agent_arrival_voucher', kwargs={'pk': pk}))
    else:
        messages.error(request, _('Arrival voucher cannot be submitted'))
        return HttpResponseRedirect(reverse('agent_arrival_voucher', kwargs={'pk': pk}))
    

def agent_arrival_voucher_print(request, pk):
    voucher = get_object_or_404(ArrivalVoucher, pk=pk, agent=request.user.agent)
    transport_movements = TransportMovement.objects.filter(voucher=voucher.pk, outside_package=False).order_by('date', 'time')
    transport_movements_outside_package = TransportMovement.objects.filter(voucher=voucher.pk, outside_package=True).order_by('date', 'time')

    context = {
        'voucher': voucher,
        'transport_movements': transport_movements,
        'transport_movements_outside_package': transport_movements_outside_package,
    }
    return render(request, 'print/agent_transport_program.html', context)



@login_required()
def agent_code_form(request, pk):
    agent_instance = get_object_or_404(Agent, pk=pk, company=request.user.employee.company)
    
    if request.method == "POST":
        formset = AgentCodeFormset(request.POST, instance=agent_instance, queryset=AgentCode.objects.filter(agent__id=agent_instance.id))
        if formset.is_valid():
            formset.save()
            # Optionally, you can add a success message here
            messages.success(request, _('Agent codes have been updated successfully.'))
            return render(request, "close_popup.html")
            

    else:
        formset = AgentCodeFormset(instance=agent_instance, queryset=AgentCode.objects.filter(agent__id=agent_instance.id))

    context = {
        "agent": agent_instance,
        "agent_code_formset": formset
    }
    return render(request, "popup_forms/agent_code.html", context)


def agent_commission_form(request, pk):
    agent_instance = get_object_or_404(AgentCommission, agent__pk=pk, company=request.user.employee.company)
    form = AgentCommissionForm(instance=agent_instance)
    if request.method == "POST":
        form = AgentCommissionForm(request.POST, instance=agent_instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('Agent commission has been updated successfully.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Error while updating agent commission'))
    context = {
        "agent": agent_instance,
        "form": form,
        "title": _("Agent Commission") + " - " + str(agent_instance)
    }
    return render(request, "form.html", context)


@login_required
def agent_account_view(request):
    from account.models import Account, JournalEntry
    from decimal import Decimal
    agent = get_object_or_404(Agent, id=request.user.agent.id, can_view_account_statement=True) 
    account = Account.objects.get(pk=agent.account.pk)
    journal_entries = JournalEntry.objects.filter(account=account).order_by('date', 'pk')
    balance = Decimal(0.00)


   

    entries = []
    for entry in journal_entries:
        balance += Decimal(entry.entry_amount())
        entries.append({
            'entry': entry,
            'balance': balance,
        })




    



    context = {'account': account, 'journal_entries': entries, 'agent':True}
    return render(request, 'account.html', context)
