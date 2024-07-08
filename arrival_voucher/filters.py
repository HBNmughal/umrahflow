import django_filters
from django_filters import DateFilter, ChoiceFilter, DateFromToRangeFilter, widgets, ModelChoiceFilter
from agent.models import Agent
from django import forms
from company.models import Employee
from company.models import Company
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from transport.models import TransportMovement



class OperatingScheduleFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        field_name='voucher__type', 
        queryset=TransportMovement.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        # method = "filter_agent"

    )
    agent = django_filters.ModelChoiceFilter(
        field_name='agent', 
        queryset=Agent.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        # method = "filter_agent"

    )   
    class Meta:
        model = TransportMovement
        fields = ['type', 'agent']

