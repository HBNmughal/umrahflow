from django import forms
from .models import UmrahVisaGroupInvoiceDefaultPrices, UmrahVisaGroupInvoice
# inlineformset_factory
from django.forms.models import inlineformset_factory

class UmrahVisaGroupInvoiceDefaultPricesForm(forms.ModelForm):
    class Meta:
        model = UmrahVisaGroupInvoiceDefaultPrices
        fields = [
            'company',
            'ground_service_price',
            'visa_fees',
            'insurance_fees',
            'electronic_services_fees',
            'transport_brn',
            'hotel_brn',
        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'ground_service_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'visa_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'insurance_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'electronic_services_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_brn': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel_brn': forms.NumberInput(attrs={'class': 'form-control'}),
    }


class UmrahVisaGroupInvoiceForm(forms.ModelForm):
    class Meta:
        model = UmrahVisaGroupInvoice
        fields = [
            'date',
            'agent',
            'voucher_no',
            'group_no',
            'pax',
            'transport_included',
            'visa_fees',
            'insurance_fees',
            'electronic_services_fees',
            'transport_brn',
            'hotel_brn',
            'ground_service_price',
            'visa_sale_price',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'agent': forms.Select(attrs={'class': 'form-control select2'}),
            'group_no': forms.TextInput(attrs={'class': 'form-control'}),
            'voucher_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pax': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1'}),
            'visa_sale_price': forms.NumberInput(attrs={'class': 'form-control', "readonly": "readonly"}),
            'transport_included': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', }),
            'ground_service_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'visa_fees': forms.NumberInput(attrs={'class': 'form-control', "readonly": "readonly"}),
            'insurance_fees': forms.NumberInput(attrs={'class': 'form-control', "readonly": "readonly"}),
            'electronic_services_fees': forms.NumberInput(attrs={'class': 'form-control', "readonly": "readonly"}),
            'transport_brn': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel_brn': forms.NumberInput(attrs={'class': 'form-control'}),
        }



