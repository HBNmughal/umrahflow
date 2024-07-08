from django import forms
from .models import  AgentVoucher, FixedVoucherPrices, TransportInvoice
from django.utils.translation import gettext_lazy as _
from django.conf import settings
def c_user(request):
    return request.user


class AgentVoucherForm(forms.ModelForm):
    class Meta:
        model = AgentVoucher
        fields = ("company", "voucher_no",  "pax", "date", "group_no", "agent", "extra_fees")
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.Select(attrs={"class": "form-control select2"}),
            "voucher_no": forms.TextInput(attrs={"class": "form-control"}),
           
            "pax": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date', "dir":"rtl"}),
            "group_no": forms.TextInput(attrs={"class": "form-control"}),
            "extra_fees": forms.NumberInput(attrs={"class": "form-control"}),
        }

class TransportInvoiceForm(forms.ModelForm):
    class Meta:
        model = TransportInvoice
        fields = (
            "company",
            "agent",
            "date",
            "transport_type",
            "description",
            "arrival_voucher",
            "referance_no",


            "qty",
            "price",
        )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.Select(attrs={"class": "form-control select2"}),
            "date": forms.DateInput(
                attrs={"class": "form-control",'type':'date', "dir":"rtl"}, format=('%Y-%m-%d')),
            "transport_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "qty": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "arrival_voucher": forms.Select(attrs={"class": "form-control select2"}),
            "referance_no": forms.TextInput(attrs={"class": "form-control"}),
        }

