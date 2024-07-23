from django import forms
from django import forms
from django.forms import ModelForm
from .models import ArrivalVoucher
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, ButtonHolder, Submit, Field
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, InlineRadios, FormActions
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.forms import modelformset_factory
from agent.models import Agent
from transport.models import TransportCompany, TransportType




class ArrivalVoucherGroupDetailsForm(forms.ModelForm):
    
    class Meta:
        model = ArrivalVoucher
        fields = [
            'agent',
            'country',
            'group_name',
            'group_no',
            'pax',
            'group_leader',
            'group_leader_contact',
            'agent_referance_no',
            'voucher_remarks',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(),
            'country': forms.Select(attrs={'class': 'form-control select2'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pax': forms.NumberInput(attrs={'class': 'form-control'}),
            'group_leader': forms.TextInput(attrs={'class': 'form-control'}),
            'group_leader_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_referance_no': forms.TextInput(attrs={'class': 'form-control'}),
            'voucher_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'agent': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'company': _('Company'),
            'agent': _('Agent'),
            'country': _('Country'),
            'group_name': _('Group name'),
            'group_no': _('Group no'),
            'pax': _('PAX'),
            'group_leader': _('Group leader name'),
            'group_leader_contact': _('Group leader contact'),

        }
    
        
class ArrivalVoucherFlightDetailsForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'arrival_flight_no',
            'arrival_date',
            'arrival_time',
            'arrival_airport',
            'departure_flight_no',
            'departure_date',
            'departure_time',
            'departure_airport',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(),
            'arrival_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(
                attrs={"class": "form-control",'type':'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'arrival_airport': forms.Select(attrs={'class': 'form-control select2'}),
            'departure_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'departure_airport': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'company': _('Company'),
            'arrival_flight_no': _('Arrival flight no'),
            'arrival_date': _('Arrival date'),
            'arrival_time': _('Arrival time'),
            'arrival_airport': _('Arrival airport'),
            'departure_flight_no': _('Departure flight no'),
            'departure_date': _('Departure date'),
            'departure_time': _('Departure time'),
            'departure_airport': _('Departure airport'),
        }

class ArrivalVoucherAccommodationDetailsForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'makkah_hotel',
            'medina_hotel',
            'company',
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'makkah_hotel': forms.TextInput(attrs={'class': 'form-control'}),
            'medina_hotel': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GroupLeaderForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'group_leader',
            'group_leader_contact',
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'group_leader': forms.TextInput(attrs={'class': 'form-control'}),
            'group_leader_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TransportBrnForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            # 'transport_package',
            'transport_type',
            'transport_company',
            'transport_brn',
            'transport_status',
            'transport_remarks',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(),
            'transport_type': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_brn': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_status': forms.Select(attrs={'class': 'form-control select2'}),
            'package_purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'transport_package': forms.Select(attrs={'class': 'form-control select2'}),
        }

from django import forms
from django import forms
from django.forms import ModelForm
from .models import ArrivalVoucher
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, ButtonHolder, Submit, Field
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, InlineRadios, FormActions
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.forms import modelformset_factory


class RawdahPermitForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'rawdah_men_request_date',
            'rawdah_men_reservation_date',
            'rawdah_men_reservation_time',
            'rawdah_men_status',
            'rawdah_women_request_date',
            'rawdah_women_reservation_date',
            'rawdah_women_reservation_time',
            'rawdah_women_status',
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'rawdah_men_request_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'rawdah_women_request_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'rawdah_men_reservation_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'rawdah_men_reservation_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'rawdah_men_status': forms.Select(attrs={'class': 'form-control select2'}),
            'rawdah_women_reservation_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'rawdah_women_reservation_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'rawdah_men_status': forms.Select(attrs={'class': 'form-control select2'}),
            'rawdah_women_status': forms.Select(attrs={'class': 'form-control select2'}),

        }
 



class ArrivalVoucherForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'agent',
            'group_name',
            'group_no',
            'pax',
            'group_leader',
            'group_leader_contact',
            'agent_referance_no',
            'arrival_flight_no',
            'arrival_date',
            'arrival_time',
            'arrival_airport',
            'departure_flight_no',
            'departure_date',
            'departure_time',
            'departure_airport',
            'makkah_hotel',
            'medina_hotel',
            'transport_type',
            'transport_company',
            'transport_brn',
            'transport_status'

        ]
        widgets = {
            'company': forms.HiddenInput(),
            'agent': forms.Select(attrs={'class': 'form-control select2'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pax': forms.NumberInput(attrs={'class': 'form-control'}),
            'group_leader': forms.TextInput(attrs={'class': 'form-control'}),
            'group_leader_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_referance_no': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'arrival_airport': forms.Select(attrs={'class': 'form-control select2'}),
            'departure_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'departure_airport': forms.Select(attrs={'class': 'form-control select2'}),
            'makkah_hotel': forms.TextInput(attrs={'class': 'form-control'}),
            'medina_hotel': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_brn': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_status': forms.Select(attrs={'class': 'form-control select2'}),


        }

class ArrivalVoucherForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'agent',
            'group_name',
            'group_no',
            'pax',
            'group_leader',
            'group_leader_contact',
            'agent_referance_no',
            'arrival_flight_no',
            'arrival_date',
            'arrival_time',
            'arrival_airport',
            'departure_flight_no',
            'departure_date',
            'departure_time',
            'departure_airport',
            'makkah_hotel',
            'medina_hotel',
            'transport_type',
            'transport_company',
            'transport_brn',
            'transport_status'
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'agent': forms.Select(attrs={'class': 'form-control select2'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pax': forms.NumberInput(attrs={'class': 'form-control'}),
            'group_leader': forms.TextInput(attrs={'class': 'form-control'}),
            'group_leader_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_referance_no': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'arrival_airport': forms.Select(attrs={'class': 'form-control select2'}),
            'departure_flight_no': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time'}),
            'departure_airport': forms.Select(attrs={'class': 'form-control select2'}),
            'makkah_hotel': forms.TextInput(attrs={'class': 'form-control'}),
            'medina_hotel': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2'}),
            'transport_brn': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_status': forms.Select(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArrivalVoucherForm, self).__init__(*args, **kwargs)
        self.fieldsets = (
            ('Group Information', {
                'fields': ('group_name', 'group_no', 'pax', 'group_leader', 'group_leader_contact', 'agent_referance_no'),
            }),
            ('Arrival Information', {
                'fields': ('arrival_flight_no', 'arrival_date', 'arrival_time', 'arrival_airport'),
            }),
            ('Departure Information', {
                'fields': ('departure_flight_no', 'departure_date', 'departure_time', 'departure_airport'),
            }),
            ('Hotel Information', {
                'fields': ('makkah_hotel', 'medina_hotel'),
            }),
            ('Transport Information', {
                'fields': ('transport_type', 'transport_company', 'transport_brn', 'transport_status'),
            }),
        )


class ArrivalVoucherApprovalForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'status',
            'rejected_reason',
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'rejected_reason': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': _('Status'),
            'rejected_reason': _('Rejected Reason'),
        }
        
class ArrivalVoucherAccountsForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            # 'accounts_remarks',
            # 'accounts_status',
            
        ]

mandoob_city = (
    ('', _('All')),
    ('makkah', _('Makkah')),
    ('madinah', _('Medina')),
    ('medina_airport', _('Medina Airport')),
    ('jeddah_airport', _('Jeddah Airport')),
)


class OperatingScheduleFilterForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'date'}), label=_('Date'))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2 '}), label=_('Agent'))
    transport_company = forms.ModelChoiceField(queryset=TransportCompany.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Transport Company'))
    transport_type = forms.ModelChoiceField(queryset=TransportType.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Transport Type'))
    schedule_for = forms.ChoiceField(choices=mandoob_city, required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Schedule For'))




class ArrivalVoucherFilterForm(forms.Form):
    voucher = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Voucher No'))
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2 '}), label=_('Agent'))
    agent_referance_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Agent Reference No'))
    transport_company = forms.ModelChoiceField(queryset=TransportCompany.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Transport Company'))
    transport_type = forms.ModelChoiceField(queryset=TransportType.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Transport Type'))
    transport_brn = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Transport BRN'))
    pax = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}), label=_('PAX'))
    group_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Group No'))
    group_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Group Name'))
    transport_status = forms.ChoiceField(choices=(('', _('All')), ('pending', _('Pending')), ('approved', _('Approved')), ('rejected', _('Rejected'))), required=False, widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Transport Status'))
    