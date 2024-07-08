from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from arrival_voucher.models import ArrivalVoucher
from django.forms import formset_factory, inlineformset_factory
from transport.models import TransportMovement


class ArrivalVoucherPurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'transport_company',
            'transport_type',
            'package_purchase_amount',
        ]

        widgets = {
            'company': forms.HiddenInput(attrs={}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2', 'disabled': True}),
            'transport_type': forms.Select(attrs={'class': 'form-control select2', 'disabled': True}),
            'package_purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'company': _('Company'),
            'transport_company': _('Transport Company'),
            'transport_type': _('Transport Type'),
            'package_purchase_amount': _('Package Purchase Price'),
        }


class ArrivalVoucherSaleInvoiceForm(forms.ModelForm):
    class Meta:
        model = ArrivalVoucher
        fields = [
            'company',
            'agent',
            'pax',
            'package_sale_amount',
        ]

        widgets = {
            'company': forms.HiddenInput(attrs={}),
            'agent': forms.Select(attrs={'class': 'form-control select2', 'disabled': True}),
            'pax': forms.NumberInput(attrs={'class': 'form-control', 'disabled': True}),
            'package_sale_amount': forms.NumberInput(attrs={'class': 'form-control',}),
        }


        labels = {
            'company': _('Company'),
            'agent': _('Agent'),
            'pax': _('PAX'),
            'package_sale_amount': _('Package Sale Price'),

        }




class TransportMovementIncludedPackageForm(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'company',
            'voucher',
            'agent',
            'route',
            'date',
            'remarks',
            'type',
            


            ]
        widgets = {
            'company': forms.HiddenInput(),
            'voucher': forms.HiddenInput(),
            'agent': forms.HiddenInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'route': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none; ', 'readonly': True}),
            'type': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'transport_company': forms.Select(attrs={'class': 'form-control ' ,'style': 'border: 0; box-shadow: none;', 'readonly':True}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'status': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'outside_package': forms.CheckboxInput(attrs={}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
            'sale_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;', 'readonly': True}),
        }
TransportMovementIncludedPackageFormset = inlineformset_factory(ArrivalVoucher, TransportMovement, form=TransportMovementIncludedPackageForm,
                                                extra=0,
                                                can_delete=False,
                                                

                                                  )

class TransportMovementOutsidePackageForm(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'company',
            'voucher',
            'route',
            'date',
            'status',
            'remarks',
            'type',
            'transport_company',
            'purchase_amount',
            'sale_amount',
            ]
        widgets = {
            'company': forms.HiddenInput(),
            'voucher': forms.HiddenInput(),
            'route': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none; ', 'readonly': True}),
            'type': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none;','readonly': True}),
            'transport_company': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none; ','readonly': True }),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'border: 0; box-shadow: none;','readonly': True }),
            'status': forms.Select(attrs={'class': 'form-control ', 'style': 'border: 0; box-shadow: none;','readonly': True}),
            'outside_package': forms.CheckboxInput(attrs={'readonly': True}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'sale_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;','readonly': True}),
        }
        labels = {
            'company': _('Company'),
            'voucher': _('Voucher'),
            'route': _('Route'),
            'date': _('Date'),
            'status': _('Status'),
            'remarks': _('Remarks'),
            'type': _('Type'),  
            'transport_company': _('Transport Company'),
            'purchase_amount': _('Purchase Amount'),
            'sale_amount': _('Sale Amount'),
        }


TransportMovementOutsidePackageFormset = inlineformset_factory(ArrivalVoucher, TransportMovement, form=TransportMovementOutsidePackageForm,can_delete=False, extra=0, max_num=10,)




    

