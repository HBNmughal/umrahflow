from django import forms
from .models import Mandoob
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



# class Mandoob(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name=_('Company'))
#     name = models.CharField(max_length=100, verbose_name=_('Name'))
#     phone = models.CharField(max_length=20, verbose_name=_('Phone'))
#     city = models.CharField(max_length=20, choices=mandoob_city, verbose_name=_('City'))
#     address = models.CharField(max_length=100, verbose_name=_('Address'))
#     username = models.CharField(max_length=100, verbose_name=_('Username'))
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name=_('User'))


class MandoobForm(forms.ModelForm):
    class Meta:
        model = Mandoob
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'company': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'token': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

        }
        labels = {
            'company': _('Company'),
            'name': _('Name'),
            'phone': _('Phone'),
            'city': _('City'),
            'address': _('Address'),
            'username': _('Username'),
        }
