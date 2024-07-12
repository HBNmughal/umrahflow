from django import forms
from company.models import Employee, Designation, SystemSettings
from django.utils.translation import gettext_lazy as _




class EmployeeForm(forms.ModelForm): 
    class Meta:
        model = Employee
        fields = ("company",
                'id_no',
                'name',
                'designation',
                'salary','is_active' )

        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "id_no": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "designation": forms.Select(attrs={"class": "form-control select2"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}), 
            # "is_active": forms.RadioSelect(attrs={'class': ''})

        }

class DesignationForm(forms.ModelForm): 
    class Meta:
        model = Designation
        fields = ("company", 'designation_en', 'designation_ar' )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "designation_en": forms.TextInput(attrs={"class": "form-control"}),
            "designation_ar": forms.TextInput(attrs={"class": "form-control"}),
      

        }

class AccountsSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ("company",
                    "default_currency",
                    "virtual_agents_account",
                    "external_agents_account",
                    "transport_company_account_tree",
                    "transport_expense_account",
                    "gib_main_account",
                    "gib_virtual_account",
                    "settlement_account",
                    "umrah_visa_purchase_account",
                    "umrah_visa_sales_account",
                    "transport_purchase_account",
                    "transport_sales_account",
                    "vat_account",
                    "agent_commission_account",
                    "account_statement_note",
                    "edit_hours",
                    "delete_hours"
                    )
        widgets = {
            "company": forms.HiddenInput(attrs={}),
            "default_currency": forms.Select(attrs={"class": "form-control"}),
            "virtual_agents_account": forms.Select(attrs={"class": "form-control"}),
            "external_agents_account": forms.Select(attrs={"class": "form-control"}),
            "transport_company_account_tree": forms.Select(attrs={"class": "form-control"}),
            "transport_expense_account": forms.Select(attrs={"class": "form-control"}),
            "gib_main_account": forms.Select(attrs={"class": "form-control"}),
            "gib_virtual_account": forms.Select(attrs={"class": "form-control"}),
            "settlement_account": forms.Select(attrs={"class": "form-control"}),
            "umrah_visa_purchase_account": forms.Select(attrs={"class": "form-control"}),
            "umrah_visa_sales_account": forms.Select(attrs={"class": "form-control"}),
            "transport_purchase_account": forms.Select(attrs={"class": "form-control"}),
            "transport_sales_account": forms.Select(attrs={"class": "form-control"}),
            "vat_account": forms.Select(attrs={"class": "form-control"}),
            "agent_commission_account": forms.Select(attrs={"class": "form-control"}),
            "account_statement_note": forms.Textarea(attrs={"class": "form-control"}),
            "edit_hours": forms.NumberInput(attrs={"class": "form-control"}),
            "delete_hours": forms.NumberInput(attrs={"class": "form-control"}),
        }