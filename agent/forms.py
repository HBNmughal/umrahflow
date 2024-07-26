from django import forms
from django.forms import formset_factory, inlineformset_factory


from .models import Agent, AgentPrice, AgentCode, AgentCommission
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import Agent, AgentPrice, AgentCode, AgentCommission
from django.utils.translation import gettext_lazy as _

def c_user(request):
    return request.user
class AgentForm(forms.ModelForm):
    
    class Meta:
        model = Agent
        fields = ("company", "country", "code", "agent_type", "name_en", "name_ar", "address", "contact", 'can_view_account_statement')

        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "country": forms.Select(attrs={"class": "form-control select2"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "agent_type": forms.Select(attrs={"class": "form-control select2"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_ar": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control"}),
            "contact": forms.Textarea(attrs={"class": "form-control"}),
            "can_view_account_statement": forms.CheckboxInput(attrs={"class": "form-control", "type": "checkbox"}),
        }
        
class AgentPriceForm(forms.ModelForm):
    
    class Meta:
        model = AgentPrice
        fields = ("agent", 'date', "visa_price", "visa_included_transport_price" , 'transport_included_by_default')

        widgets = {
            "agent": forms.HiddenInput(attrs={}),
            "date": forms.DateInput(attrs={"class": "form-control datepicker", "type": "date"}),
            "visa_price": forms.NumberInput(attrs={"class": "form-control"}),
            "visa_included_transport_price": forms.NumberInput(attrs={"class": "form-control"}),
            "transport_included_by_default": forms.CheckboxInput(attrs={"class": "form-control", "type": "checkbox"}),
            
        }
    labels = {
        "agent": _("Agent"),
        "date": _("From Date"),
        "price": _("Visa Price"),
        "transport_price": _("Transport Price"),
        "transport_included_by_default": _("Transport Included By Default"),
    }



class AgentCodeForm(forms.ModelForm):
    class Meta:
        model = AgentCode
        fields = ( 'agent', "platform", "country", "code")

        widgets = {
            "agent": forms.HiddenInput(attrs={}),
            "platform": forms.Select(attrs={'class':'form-control select2'}),
            "country": forms.Select(attrs={'class':'form-control select2'}),
            "code": forms.TextInput(attrs={'class':'form-control'}),
        }
    labels = {
        "country": _("Country"),
        "agent": _("Agent"),
        "platform": _("Platform"),
        "country": _("Country"),
        "code": _("Code"), 
        }
    

AgentCodeFormset = inlineformset_factory(Agent, AgentCode, form=AgentCodeForm,extra=10,)


class AgentCommissionForm(forms.ModelForm):
    class Meta:
        model = AgentCommission
        fields = ("company", "agent", "comission_holder_account", "date", "commission_per_visa_with_transport", "commission_per_visa_without_transport")

        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.Select(attrs={"class": "form-control select2"}),
            "comission_holder_account": forms.Select(attrs={"class": "form-control select2"}),
            "date": forms.DateInput(attrs={"class": "form-control datepicker", "type": "date"}),
            "commission_per_visa_with_transport": forms.NumberInput(attrs={"class": "form-control"}),
            "commission_per_visa_without_transport": forms.NumberInput(attrs={"class": "form-control"}),
        }
    labels = {
        "company": _("Company"),
        "agent": _("Agent"),
        "comission_holder_account": _("Comission Holder Account"),
        "date": _("Change Date"),
        "commission_per_visa_with_transport": _("Commission Per Visa With Transport"),
        "commission_per_visa_without_transport": _("Commission Per Visa Without Transport"),
    }



class AgentCommissionForm(forms.ModelForm):
    class Meta:
        model = AgentCommission
        fields = ("company", "agent", "comission_holder_account", "date", "commission_per_visa_with_transport", "commission_per_visa_without_transport")

        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.HiddenInput(attrs={}),
            "comission_holder_account": forms.Select(attrs={"class": "form-control select2"}),
            "date": forms.DateInput(attrs={"class": "form-control datepicker", "type": "date"}),
            "commission_per_visa_with_transport": forms.NumberInput(attrs={"class": "form-control"}),
            "commission_per_visa_without_transport": forms.NumberInput(attrs={"class": "form-control"}),
        }
    labels = {
        "company": _("Company"),
        "agent": _("Agent"),
        "comission_holder_account": _("Comission Holder Account"),
        "date": _("Change Date"),
        "commission_per_visa_with_transport": _("Commission Per Visa With Transport"),
        "commission_per_visa_without_transport": _("Commission Per Visa Without Transport"),
    }

