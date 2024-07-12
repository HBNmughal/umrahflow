from django import forms
from .models import Account, ReceiptVoucher, PaymentVoucher, AccountSettlementCredit, AccountSettlementDebit, JournalEntry
from django.utils.translation import gettext_lazy as _
from django import forms
import calculation




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'company', 
            'account_name_en', 
            'account_name_ar', 
            'parent_account',
            'account_type',
        ]
        widgets = {
            'company': forms.HiddenInput(),
            'account_name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'account_name_ar': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_account': forms.Select(attrs={'class': 'form-control'}),
            'account_type': forms.HiddenInput(attrs={}),
        }
        labels = {
            'company': _('Company'),
            'account_name_en': _('Account Name (English)'),
            'account_name_ar': _('Account Name (Arabic)'),
            'parent_account': _('Parent Account'),
            'allow_child_accounts': _('Allow Child Accounts'),
            'account_type': _('Account Type'),
            
        }
        help_texts = {
            'company': (''),
            'account_name_en': (''),
            'account_name_ar': (''),
            'parent_account': (''),
            'allow_child_accounts': (''),
            'account_type': (''),
        }
        

class ReceiptVoucherForm(forms.ModelForm):
    class Meta:
        model = ReceiptVoucher
        fields = [
            'date',
            'collected_from',
            'collected_from_name',
            'to_account',
            'amount',
            'description',
            'payment_method',
            'reference_no',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'collected_from': forms.Select(attrs={'class': 'form-control select2'}),
            'collected_from_name': forms.TextInput(attrs={'class': 'form-control'}),
            'to_account': forms.Select(attrs={'class': 'form-control select2'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'company': _('Company'),
            'date': _('Date'),
            'transaction': _('Transaction'),
            'collected_from': _('Collected From'),
            'collected_from_name': _('Collected From Name'),
            'to_account': _('To Account'),
            'amount': _('Amount'),
            'description': _('Description'),
            'reference_no': _('Reference No'),
            'payment_method': _('Payment Method'),
        }
        help_texts = {
            'company': (''),
            'date': (''),
            'transaction': (''),
            'collected_from': (''),
            'collected_from_name': (''),
            'to_account': (''),
            'amount': (''),
            'description': (''),
            'reference_no': (''),
            'payment_method': (''),
        }

class PaymentVoucherForm(forms.ModelForm):
    class Meta:
        model = PaymentVoucher
        fields = [
            'date',
            'paid_to',
            'paid_to_name',
            'from_account',
            'amount',
            'description',
            'payment_method',
            'reference_no',
            'company',

        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_to': forms.Select(attrs={'class': 'form-control select2'}),
            'paid_to_name': forms.TextInput(attrs={'class': 'form-control'}),
            'from_account': forms.Select(attrs={'class': 'form-control select2'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'company': _('Company'),
            'date': _('Date'),
            'transaction': _('Transaction'),
            'paid_to': _('Paid To'),
            'paid_to_name': _('Paid To Name'),
            'from_account': _('From Account'),
            'amount': _('Amount'),
            'description': _('Description'),
            'reference_no': _('Reference No'),
            'payment_method': _('Payment Method'),
        }
        help_texts = {
            'company': (''),
            'date': (''),
            'transaction': (''),
            'paid_to': (''),
            'paid_to_name': (''),
            'from_account': (''),
            'amount': (''),
            'description': (''),
            'reference_no': (''),
            'payment_method': (''),
        }

class AccountSettlementCreditForm(forms.ModelForm):
    class Meta:
        model = AccountSettlementCredit
        fields = [
            'company',
            'date',
            'credit_account',
            'amount',
            'description',
            'reference_no',
            
        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'credit_account': forms.HiddenInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'class': 'form-control'}),        }
        labels = {
            'company': _('Company'),
            'date': _('Date'),
            'transaction': _('Transaction'),
            'credit_account': _('Credit Account'),
            'amount': _('Amount'),
            'description': _('Description'),
            'reference_no': _('Reference No'),
            'payment_method': _('Payment Method'),
        }
        help_texts = {
            'company': (''),
            'date': (''),
            'transaction': (''),
            'credit_account': (''),
            'amount': (''),
            'description': (''),
            'reference_no': (''),
            'payment_method': (''),
        }


class AccountSettlementDebitForm(forms.ModelForm):
    class Meta:
        model = AccountSettlementDebit
        fields = [
            'company',
            'date',
            'debit_account',
            'amount',
            'description',
            'reference_no',
            
        ]
        widgets = {
            'company': forms.HiddenInput(attrs={'class': ''}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'debit_account': forms.HiddenInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'class': 'form-control'}),        }
        labels = {
            'company': _('Company'),
            'date': _('Date'),
            'transaction': _('Transaction'),
            'debit_account': _('Debit Account'),
            'amount': _('Amount'),
            'description': _('Description'),
            'reference_no': _('Reference No'),
            'payment_method': _('Payment Method'),
        }
        help_texts = {
            'company': (''),
            'date': (''),
            'transaction': (''),
            'debit_account': (''),
            'amount': (''),
            'description': (''),
            'reference_no': (''),
            'payment_method': (''),
        }


class LedgerEntryForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.Select(attrs={'class': 'form-control select2'}), label=_('Account'))
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Description'))
    debit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control debit_input'}), initial=0.00, label=_('Debit'))
    credit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control credit_input'}), initial=0.00, label=_('Credit'))
    

LedgerEntryFormSet = forms.formset_factory(LedgerEntryForm, extra=50)

class TransactionForm(forms.Form):
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Description'))
    reference_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label=_('Reference No'))
    total_debit = forms.DecimalField(widget=calculation.SummaryInput(function=calculation.SUM, field='debit',attrs={'readonly': 'readonly', 'class':'form-control'}), initial=0.00, label=_('Total Debit'))
    total_credit = forms.DecimalField(widget=calculation.SummaryInput(function=calculation.SUM, field='credit',attrs={'readonly': 'readonly', 'class':'form-control'}), initial=0.00, label=_('Total Credit'))