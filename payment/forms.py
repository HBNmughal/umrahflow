from django import forms
from .models import AgentPaymentTransaction, OfficeExpense, CompanyTreasuryTransaction, Payroll
from django.utils.translation import gettext_lazy as _



WithdrawPaymentOptions = (
    ("d", _("Main Account")),
    ("rd", _("Agent Return")),
    ("cod", _("Commission")),

)

class AgentCollectPayment(forms.ModelForm): 
    class Meta:
        model = AgentPaymentTransaction
        fields = ("company", "agent", "amount",'date',"transaction_type", 'payment_for',"payment_by","performed_by",
                #   'received_to_account'
                  )

        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "transaction_type": forms.HiddenInput(attrs={"value": "c"}),
            "agent": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control",'type':'date'}),
            "payment_by": forms.Select(attrs={"class": "form-control select2"}),
            "payment_for": forms.TextInput(attrs={"class": 'form-control'}),
            # "received_to_account": forms.Select(attrs={"class": 'form-control select2', "required": True}),
            "performed_by": forms.TextInput(attrs={"class": "form-control"}),

        }

        labels = {
            "received_to_account": _("Received To Account"),
            "performed_by": _("Accountant"),

        }

class AgentWithdrawPayment(forms.ModelForm): 
    class Meta:
        model = AgentPaymentTransaction
        fields = ("company", "agent", "amount","transaction_type", "reason","payment_by","performed_by", "received_by" )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "transaction_type": forms.Select(attrs={"class": 'form-control select2'}),
            "agent": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_by": forms.Select(attrs={"class": "form-control select2"}),
            "reason": forms.HiddenInput(),
            "performed_by": forms.TextInput(attrs={"class": "form-control"}),    
            "received_by": forms.TextInput(attrs={"class": "form-control"}),


        }
        labels = {
            "performed_by": _("Accountant"),
            }

class OfficeExpenseForm(forms.ModelForm):
    class Meta:
        model = OfficeExpense
        fields = ("company", "payment_by","amount","date", "bill_no","reason","paid_to", "accountant" )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "bill_no": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),

            
            "payment_by": forms.Select(attrs={"class": "form-control select2"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
            "paid_to": forms.TextInput(attrs={"class": "form-control"}),    
            "accountant": forms.TextInput(attrs={"class": "form-control"}),
        }

class TreasuryCollectPayment(forms.ModelForm):
    class Meta:
        model = CompanyTreasuryTransaction
        fields = ("company", "amount","transaction_type","transaction_for","reason", "payment_by","date","performed_by", "received_by" )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "transaction_type": forms.HiddenInput(),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),

            
            "transaction_for": forms.HiddenInput(),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
            "payment_by": forms.Select(attrs={"class": "form-control, select2"}),

            "performed_by": forms.TextInput(attrs={"class": "form-control"}),    
            "received_by": forms.TextInput(attrs={"class": "form-control"}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ("company", "start_date", "end_date" )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),
        }

# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ("company", "account_name_en", "account_name_ar")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account_name_en": forms.TextInput(attrs={"class": "form-control"}),
#             "account_name_ar": forms.TextInput(attrs={"class": "form-control"}),

#         }

# class AccountTransferForm(forms.ModelForm):
#     class Meta:
#         model = AccountTransaction
#         fields = ("company", "account","transfer_to", "debit", "date", "discription", "document_no")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account": forms.HiddenInput(attrs={}),
#             "transfer_to": forms.Select(attrs={"class": "form-control select2"}),
#             "debit": forms.NumberInput(attrs={"class": "form-control"}),
#             "date": forms.DateTimeInput(
#                 attrs={"class": "form-control",'type':'date'}),
#             "document_no": forms.TextInput(attrs={"class": "form-control"}),
#             "discription": forms.TextInput(attrs={"class": "form-control"}),
#         }
#         labels = {
#                 'transfer_to': _('Transfer To'),
#                 'debit': _('Amount'),
#             }
        
# class AccountTransactionCreditForm(forms.ModelForm):
#     class Meta:
#         model = AccountTransaction
#         fields = ("company", "account", "received_from" , "credit", "date", "discription","document_no", "performed_by")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account": forms.HiddenInput(attrs={}),
#             "received_from": forms.TextInput(attrs={"class": "form-control"}),
#             "credit": forms.NumberInput(attrs={"class": "form-control"}),
#             "date": forms.DateTimeInput(
#                 attrs={"class": "form-control",'type':'date'}),
#             "document_no": forms.TextInput(attrs={"class": "form-control"}),
#             "discription": forms.TextInput(attrs={"class": "form-control"}),
#             "performed_by": forms.TextInput(attrs={"class": "form-control"}),
#         }
        
#         labels = {
#                 'credit': _('Amount'),
#                 "received_from": _("Received From"),
#                 "performed_by": _("Accountant"),


#             }


# class AccountTransactionDebitForm(forms.ModelForm):
#     class Meta:
#         model = AccountTransaction
#         fields = ("company", "account", "paid_to" , "debit", "date", "discription","document_no" ,"performed_by")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account": forms.HiddenInput(attrs={}),
#             "paid_to": forms.TextInput(attrs={"class": "form-control"}),
#             "debit": forms.NumberInput(attrs={"class": "form-control"}),
#             "date": forms.DateTimeInput(
#                 attrs={"class": "form-control",'type':'date'}),
#             "document_no": forms.TextInput(attrs={"class": "form-control"}),

#             "discription": forms.TextInput(attrs={"class": "form-control"}),
#             "performed_by": forms.TextInput(attrs={"class": "form-control"}),
#         }
        
#         labels = {
#                 'debit': _('Amount'),
#                 "paid_to": _("Paid To"),
#                 "performed_by": _("Accountant"),

#             }
        

class AgentSettlementTransactionCreditForm(forms.ModelForm):
    class Meta:
        model = AgentPaymentTransaction
        fields = ("company", "agent", "amount", "transaction_type", "date", "payment_for", "document_no", "performed_by", "is_settlement_transaction")
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "transaction_type": forms.HiddenInput(attrs={"value": "c"}),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),
            "document_no": forms.TextInput(attrs={"class": "form-control"}),
            "payment_for": forms.TextInput(attrs={"class": "form-control"}),
            "performed_by": forms.TextInput(attrs={"class": "form-control"}),
            "is_settlement_transaction": forms.HiddenInput(attrs={"value": True}),
        }
        labels = {
                'amount': _('Amount'),
                "performed_by": _("Accountant"),

            }
        
class AgentSettlementTransactionDebitForm(forms.ModelForm):
    class Meta:
        model = AgentPaymentTransaction
        fields = ("company", "agent", "amount", "transaction_type", "date", "payment_for", "document_no", "performed_by", "is_settlement_transaction")
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "agent": forms.HiddenInput(attrs={}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "transaction_type": forms.HiddenInput(attrs={"value": "d"}),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control",'type':'date'}),
            "document_no": forms.TextInput(attrs={"class": "form-control"}),
            "payment_for": forms.TextInput(attrs={"class": "form-control"}),
            "performed_by": forms.TextInput(attrs={"class": "form-control"}),
            "is_settlement_transaction": forms.HiddenInput(attrs={"value": True}),
        }
        labels = {
                'amount': _('Amount'),
                "performed_by": _("Accountant"),

            }

# class AccountSettlementTransactionCreditForm(forms.ModelForm):
#     class Meta:
#         model = AccountTransaction
#         fields = ("company", "account", "credit", "date", "discription", "document_no", "performed_by", "is_settlement_transaction")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account": forms.HiddenInput(attrs={}),
#             "credit": forms.NumberInput(attrs={"class": "form-control"}),
#             "date": forms.DateTimeInput(
#                 attrs={"class": "form-control",'type':'date'}),
#             "document_no": forms.TextInput(attrs={"class": "form-control"}),
#             "discription": forms.TextInput(attrs={"class": "form-control"}),
#             "performed_by": forms.TextInput(attrs={"class": "form-control"}),
#             "is_settlement_transaction": forms.HiddenInput(attrs={"value": True}),
#         }
#         labels = {
#                 'credit': _('Amount'),
#                 "performed_by": _("Accountant"),

#             }
        
# class AccountSettlementTransactionDebitForm(forms.ModelForm):
#     class Meta:
#         model = AccountTransaction
#         fields = ("company", "account", "debit", "date", "discription", "document_no", "performed_by", "is_settlement_transaction")
#         widgets = {
#             "company": forms.HiddenInput(attrs={}),
#             "account": forms.HiddenInput(attrs={}),
#             "debit": forms.NumberInput(attrs={"class": "form-control"}),
#             "date": forms.DateTimeInput(
#                 attrs={"class": "form-control",'type':'date'}),
#             "document_no": forms.TextInput(attrs={"class": "form-control"}),
#             "discription": forms.TextInput(attrs={"class": "form-control"}),
#             "performed_by": forms.TextInput(attrs={"class": "form-control"}),
#             "is_settlement_transaction": forms.HiddenInput(attrs={"value": True}),
#         }
#         labels = {
#                 'debit': _('Amount'),
#                 "performed_by": _("Accountant"),

#             }

