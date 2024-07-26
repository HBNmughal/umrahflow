# create forms here 

from django import forms
from .models import TransportRoute, TransportMovement, TransportCompany, TransportPackage, TransportType
from arrival_voucher.models import ArrivalVoucher
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory, inlineformset_factory, BaseInlineFormSet



class BaseTransportMovementFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseTransportMovementFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:

            try:
                form.fields['route'].queryset = TransportRoute.objects.filter(company=self.user.employee.company)
                form.fields['transport_company'].queryset = TransportCompany.objects.filter(company=self.user.employee.company)
                form.fields['type'].queryset = TransportType.objects.filter(company=self.user.employee.company)
            except:
                pass

class BaseTransportMovementFormSetAgent(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseTransportMovementFormSetAgent, self).__init__(*args, **kwargs)
        for form in self.forms:

            try:
                form.fields['route'].queryset = TransportRoute.objects.filter(company=self.user.agent.company)
                form.fields['type'].queryset = TransportType.objects.filter(company=self.user.agent.company)
            except:
                pass


class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        fields = ['from_en', 'from_ar', 'is_linked_with_arrival_flight','from_linked_with_makkah_hotel',
                  'from_linked_with_medina_hotel', 'to_en', 'to_ar', 'distance', 'is_linked_with_departure_flight',  
                  'to_linked_with_makkah_hotel', 'to_linked_with_medina_hotel',
                'mandoob_mark_as_on_the_way',  'mandoob_mark_as_completed', 

                  
                  ]
        labels = {
            'from_en': _('From English'),
            'from_ar': _('From Arabic'),
            'to_en': _('To English'),
            'to_ar': _('To Arabic'),
            'distance': _('Distance (km)'),
            'mandoob_mark_as_completed': _('Mandoob who can Mark as completed'),
            'mandoob_mark_as_on_the_way': _('Mandoob who can Mark as on the way'),

        }
        widgets = {
            'from_en': forms.TextInput(attrs={'class': 'form-control'}),
            'from_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'to_en': forms.TextInput(attrs={'class': 'form-control'}),
            'to_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'mandoob_mark_as_completed': forms.Select(attrs={'class': 'form-control select2'}),
            'mandoob_mark_as_on_the_way': forms.Select(attrs={'class': 'form-control select2'}),
            # should use new line for each widget

        }
    
        error_messages = {
            'from_en': {
                'max_length': _("This city name is too long."),
            },
            'from_ar': {
                'max_length': _("This city name is too long."),
            },
            'to_en': {
                'max_length': _("This city name is too long."),
            },
            'to_ar': {
                'max_length': _("This city name is too long."),
            },
            'distance': {
                'max_length': _("This distance is too long."),
            },
        }

            


class TransportMovementForm(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'company',
            'voucher',
            'agent',
            'route',
            'date',
            'time',
            'status',
            'outside_package',
            # if outside package
            
            'remarks',
            'type',
            'transport_company',

            ]
        widgets = {
            'company': forms.HiddenInput(),
            'voucher': forms.HiddenInput(),
            'agent': forms.HiddenInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'route': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none; width: 300px;'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none;width: 120px;'}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none; width: 200px;'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'border: 0; box-shadow: none;'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'style': 'border: 0; box-shadow: none;'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;width: 120px;'}),
            'status': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none;width: 120px;'}),
            'outside_package': forms.CheckboxInput(attrs={}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'sale_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(TransportMovementForm, self).__init__(*args, **kwargs)

    #     # if user is employee
    #     try:
    #         self.fields['route'].queryset = TransportRoute.objects.filter(company=user.employee.company)
    #         self.fields['transport_company'].queryset = TransportCompany.objects.filter(company=user.employee.company)
    #         self.fields['type'].queryset = TransportPackage.objects.filter(company=user.employee.company)
    #     except:
    #         pass

    #     # if user is agent
    #     try:
    #         self.fields['route'].queryset = TransportRoute.objects.filter(company=user.agent.company)
    #         self.fields['transport_company'].queryset = TransportCompany.objects.filter(company=user.agent.company)
    #         self.fields['type'].queryset = TransportPackage.objects.filter(company=user.agent.company)
    #     except:
    #         pass

       
TransportMovementFormset = inlineformset_factory(ArrivalVoucher, TransportMovement, form=TransportMovementForm,extra=6,max_num=10, formset=BaseTransportMovementFormSet)


class TransportMovementFormAgent(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'company',
            'voucher',
            'agent',
            'route',
            'date',
            'time',
            
            'remarks',
            'type',
       


            ]
        widgets = {
            'company': forms.HiddenInput(),
            'voucher': forms.HiddenInput(),
            'agent': forms.HiddenInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'route': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none; width: 500px;'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none;width: 100px;'}),
            'transport_company': forms.Select(attrs={'class': 'form-control select2' ,'style': 'border: 0; box-shadow: none; width: 200px;'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'border: 0; box-shadow: none;'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'style': 'border: 0; box-shadow: none;'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'status': forms.Select(attrs={'class': 'form-control select2', 'style': 'border: 0; box-shadow: none; width: 100px;'}),
            'outside_package': forms.CheckboxInput(attrs={}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
            'sale_amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border: 0; box-shadow: none;'}),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(TransportRouteForm, self).__init__(*args, **kwargs)

    #     # if user is employee
    #     try:
    #         self.fields['route'].queryset = TransportRoute.objects.filter(company=user.employee.company)
    #         self.fields['transport_company'].queryset = TransportCompany.objects.filter(company=user.employee.company)
    #         self.fields['type'].queryset = TransportPackage.objects.filter(company=user.employee.company)
    #     except:
    #         pass

    #     # if user is agent
    #     try:
    #         self.fields['route'].queryset = TransportRoute.objects.filter(company=user.agent.company)
    #         self.fields['transport_company'].queryset = TransportCompany.objects.filter(company=user.agent.company)
    #         self.fields['type'].queryset = TransportPackage.objects.filter(company=user.agent.company)
    #     except:
    #         pass

TransportMovementFormsetAgent = inlineformset_factory(ArrivalVoucher, TransportMovement, form=TransportMovementFormAgent,
                                                formset=BaseTransportMovementFormSetAgent,
                                                can_delete=True,
                                                extra=6,
                                                max_num=10,
                                                

                                                  )

class MovementDriverForm(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'first_driver_name',
            'first_driver_phone',
            'second_driver_name',
            'second_driver_phone',
            'no_plate',
            ]
        widgets = {
            'first_driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'second_driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'no_plate': forms.TextInput(attrs={'class': 'form-control'}),

        }


class MovementStatusForm(forms.ModelForm):
    class Meta:
        model = TransportMovement
        fields = [
            'status',
            'remarks',
            ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }



class TransportCompanyForm(forms.ModelForm):
    class Meta:
        model = TransportCompany
        fields = ['company', 'name_en', 'name_ar', 'vat_no']
        labels = {
            'name_en': _('Name English'),
            'name_ar': _('Name Arabic'),
            'vat_no': _('VAT No.'),
        }
        widgets = {
            'company': forms.HiddenInput(),
            'name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'name_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'vat_no': forms.TextInput(attrs={'class': 'form-control'}),
            # should use new line for each widget

        }


class TransportPackageForm(forms.ModelForm):
    class Meta:
        model = TransportPackage
        fields = ['company', 'package_name_en', 'package_name_ar', 'package_short_code', 'routes']
        labels = {
            'package_name_en': _('Package Name English'),
            'package_name_ar': _('Package Name Arabic'),
            'routes': _('Routes'),
        }
        widgets = {
            'company': forms.HiddenInput(),
            'package_name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'package_name_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'routes': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'package_short_code': forms.TextInput(attrs={'class': 'form-control'}),

            # should use new line for each widget
        }