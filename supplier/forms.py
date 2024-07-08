from django import forms
from supplier.models import Supplier
from django.utils.translation import gettext_lazy as _


class SupplierForm(forms.Form):
    name_en = forms.CharField(label=_("Name (English)"), widget=forms.TextInput(attrs={"class": "form-control"}))
    name_ar = forms.CharField(label=_("Name (Arabic)"), widget=forms.TextInput(attrs={"class": "form-control"}))
    cr_no = forms.CharField(label=_("CR No"), widget=forms.TextInput(attrs={"class": "form-control"}))
    vat_no = forms.CharField(label=_("VAT No"), widget=forms.TextInput(attrs={"class": "form-control"}))
    vat_percentage = forms.FloatField(label=_("VAT Percentage"), widget=forms.NumberInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label=_("Phone"), widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label=_("Address"), widget=forms.TextInput(attrs={"class": "form-control"}))
    is_transport_company = forms.BooleanField(label=_("Is Transport Company"), widget=forms.CheckboxInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(SupplierForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SupplierForm, self).clean()
        name_en = cleaned_data.get("name_en")
        name_ar = cleaned_data.get("name_ar")
        cr_no = cleaned_data.get("cr_no")
        vat_no = cleaned_data.get("vat_no")
        vat_percentage = cleaned_data.get("vat_percentage")
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        address = cleaned_data.get("address")
        is_transport_company = cleaned_data.get("is_transport_company")
        if not name_en:
            self.add_error('name_en', _('Name (English) is required'))
        if not name_ar:
            self.add_error('name_ar', _('Name (Arabic) is required'))
        if not cr_no:
            self.add_error('cr_no', _('CR No is required'))
        if not vat_no:
            self.add_error('vat_no', _('VAT No is required'))
        if not vat_percentage:
            self.add_error('vat_percentage', _('VAT Percentage is required'))
        if not email:
            self.add_error('email', _('Email is required'))
        if not phone:
            self.add_error('phone', _('Phone is required'))

        if not address:
            self.add_error('address', _('Address is required'))
        if is_transport_company is None:
            self.add_error('is_transport_company', _('Is Transport Company is required'))
        return cleaned_data
    

