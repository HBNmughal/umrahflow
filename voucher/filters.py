import django_filters
from .models import AgentVoucher, TransportInvoice
from django_filters import DateFilter, ChoiceFilter, DateFromToRangeFilter, widgets, ModelChoiceFilter
from agent.models import Agent
from django import forms
from company.models import Employee
from company.models import Company
from django.views.generic.list import ListView
from django.contrib.auth.models import User



class AgentVoucherFilter(django_filters.FilterSet):

    date = DateFromToRangeFilter(widget=widgets.RangeWidget(attrs={'class':'form-control', 'type':'date','placeholder': 'd/m/Y'}))
    agent = django_filters.ModelChoiceFilter(
        field_name='agent', 
        queryset=Agent.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        # method = "filter_agent"

    )   
    class Meta:
        model = AgentVoucher
        fields = ['date', "agent" ]
    

class TransportInvoiceFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter(widget=widgets.RangeWidget(attrs={'class':'form-control', 'type':'date','placeholder': 'd/m/Y'}))
    agent = django_filters.ModelChoiceFilter(
        field_name='agent', 
        queryset=Agent.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        # method = "filter_agent"

    )   
    class Meta:
        model = TransportInvoice
        fields = ['date', "agent" ]
