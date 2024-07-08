from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from .choices import *
from django.utils.translation import get_language
from payment.models import AgentPaymentTransaction, CompanyTreasuryTransaction
from visa_group.models import UmrahVisaGroupInvoice
from agent.models import Agent
from django.db.models import Avg, Count, Min, Sum
import base64
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from account.models import Account
import secrets
from core.choices import *

# Create your models here.
class Company(models.Model ):
    name_en = models.CharField(max_length=64, verbose_name=_("Company Name English"))
    name_ar = models.CharField(max_length=64, verbose_name=_("Company Name Arabic"))
    cr_no = models.CharField(max_length=64, verbose_name=_("C.R No."))
    permit_no = models.CharField(verbose_name=_("MOH Permit No."), max_length=4)
    address_en = models.TextField(verbose_name=_("Company Address English"), max_length=256)
    address_ar = models.TextField(verbose_name=_("Company Address English"), max_length=256)
    contact = models.TextField(verbose_name=_("Company Contact"), max_length=256)
    vat_no = models.CharField(verbose_name=_("VAT No."), max_length=64, blank=True, null=True)
    # add logo
    logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )



    umrah_season = models.IntegerField(verbose_name=_("Umrah Season"), null=True)

    def save(self, *args, **kwargs):
        # create basic accounts on create
        from arrival_voucher.models import ArrivalVoucher
        from visa_group.models import UmrahVisaGroupInvoiceDefaultPrices
        
        super().save(*args, **kwargs)
        if not Account.objects.filter(account_type="A", company=self).exists():
            Account.objects.create(account_name_en="Assets", account_name_ar="أصول",  company=self, allow_child_accounts=True, allow_edit=False, account_type="A")
        if not Account.objects.filter(account_type="L", company=self).exists():
            Account.objects.create(account_name_en="Liabilities", account_name_ar="خصوم",  company=self, allow_child_accounts=True, allow_edit=False, account_type="L")
        if not Account.objects.filter(account_type="E", company=self).exists():
            Account.objects.create(account_name_en="Equity", account_name_ar="حقوق ملكية",  company=self, allow_child_accounts=True, allow_edit=False, account_type="E")
        if not Account.objects.filter(account_type="R", company=self).exists():
            Account.objects.create(account_name_en="Revenue", account_name_ar="إيرادات",  company=self, allow_child_accounts=True, allow_edit=False, account_type="R")
        if not Account.objects.filter(account_type="X", company=self).exists():
            Account.objects.create(account_name_en="Expenses", account_name_ar="مصروفات",  company=self, allow_child_accounts=True, allow_edit=False, account_type="X")
        if not UmrahVisaGroupInvoiceDefaultPrices.objects.filter(company=self).exists():
            UmrahVisaGroupInvoiceDefaultPrices.objects.create(company=self)

        # 
        from voucher.models import UmrahVisaGroupInvoice

        vouchers = UmrahVisaGroupInvoice.objects.filter(company = self)
        for voucher in vouchers:
            voucher.save()
        
        super().save(*args, **kwargs) 

        
    def __str__(self):
        if get_language() == "ar":
            return self.name_ar
        return self.name_en
    
    def address(self):
        if get_language() == "ar":
            return self.address_ar
        return self.address_en
    def account_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='c').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='d').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)

    def due_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='r').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='rd').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)

    def commission_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='co').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='cod').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)

    def treasury_balance(self):
        credit_transactions = CompanyTreasuryTransaction.objects.filter(company=self, transaction_type='c').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = CompanyTreasuryTransaction.objects.filter(company=self, transaction_type='d').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)
    

    def report(self):
        from agent.models import Agent

        r = {}
        r['total_pilgrims'] = UmrahVisaGroupInvoice.objects.filter(company = self).aggregate(Sum("pax")) or 0
        r['total_groups'] = UmrahVisaGroupInvoice.objects.filter(company = self).count() or 0
        r['total_agents'] = Agent.objects.filter(company = self).count() or 0
        


    def __str__(self):
        if get_language() == "ar":
            return self.name_ar
        return self.name_en

    def account_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='c').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='d').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)
    def due_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='r').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='rd').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)

    def commission_balance(self):
        credit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='co').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = AgentPaymentTransaction.objects.filter(company=self, transaction_type='cod').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)
    
    def treasury_balance(self):
        credit_transactions = CompanyTreasuryTransaction.objects.filter(company=self, transaction_type='c').aggregate(Sum('amount'))
        if credit_transactions['amount__sum'] is None:
            credit_transactions = 0.00
        else:
            credit_transactions = credit_transactions['amount__sum']
        debit_transactions = CompanyTreasuryTransaction.objects.filter(company=self, transaction_type='d').aggregate(Sum('amount'))
        if debit_transactions['amount__sum'] is None:
            debit_transactions = 0.00
        else:
            debit_transactions = debit_transactions['amount__sum']
        balance = float(credit_transactions) - float(debit_transactions)
        return round(balance, 2)

    def report(self):

        r = {}
        r['total_pilgrims'] = UmrahVisaGroupInvoice.objects.filter(company = self).aggregate(Sum("pax")) or 0
        r['total_groups'] = UmrahVisaGroupInvoice.objects.filter(company = self).count() or 0
        r['total_agents'] = Agent.objects.filter(company = self).count() or 0
        # r['total_agents'] = Agent.objects.filter(company = self).count()
        return r
    
    def email(self):
        try:
            email = CompanyEmail.objects.get(company=self)
            conf = {
                'host': email.host,
                'port': email.port,
                'use_tls': email.use_tls,
                'username': email.username,
                'password': email.password,
            }
            return conf
        except:
            return None
        

    def arrival_vouchers_pending(self):
        from arrival_voucher.models import ArrivalVoucher
        return ArrivalVoucher.objects.filter(company=self, status='pending').count()
    
    def arrival_vouchers_approved(self):
        from arrival_voucher.models import ArrivalVoucher
        return ArrivalVoucher.objects.filter(company=self, status='approved').count()
    
    def arrival_vouchers_rejected(self):
        from arrival_voucher.models import ArrivalVoucher
        return ArrivalVoucher.objects.filter(company=self, status__in=['rejected', 'with_agent_rejected']).count()
    
    def arrival_vouchers_total(self):
        from arrival_voucher.models import ArrivalVoucher
        return ArrivalVoucher.objects.filter(company=self).count()
    
    def settings(self):
        return SystemSettings.objects.get(company=self)
    

    def agents_total_debit(self):
        return AgentPaymentTransaction.objects.filter(company=self, transaction_type='d').aggregate(Sum('amount'))['amount__sum']
    
    def agents_total_credit(self):
        return AgentPaymentTransaction.objects.filter(company=self, transaction_type='c').aggregate(Sum('amount'))['amount__sum']

class Designation(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    designation_en = models.CharField(max_length=64, verbose_name=_('Designation name english'))
    designation_ar = models.CharField(max_length=64, verbose_name=_('Designation name arabic'))
    history = HistoricalRecords(
        user_model='auth.User',
    )

    def __str__(self):
        return self.designation_ar





class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    id_no = models.CharField(verbose_name=_("ID No"), max_length=10,  default="")
    name = models.CharField(verbose_name=_("Name"),max_length=64)
    designation = models.ForeignKey('company.Designation', verbose_name=_("Designation"), on_delete=models.PROTECT, null=True, blank=True)
    role = models.CharField(max_length=32, choices=user_roles, null=True,blank=True)
    token = models.CharField(max_length=256, blank=True, null=True)
    salary = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Monthly Salary"), default=0.00)
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    current_app = models.CharField(verbose_name=_("Current Application"),max_length=64, blank=True, null=True)

    history = HistoricalRecords(
        user_model='auth.User',
    )

    def __str__(self):
        return self.name
    def save(self, request=None, *args, **kwargs):
        if self.token is None:
            self.token = (base64.b32encode(bytearray('umrahflow'+str(str(self.user.employee.company.permit_no)+(self.user.username)), 'ascii')).decode('utf-8')).replace('=', '')
        super().save(*args, **kwargs)


    
class CompanyEmail(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, unique=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    use_tls = models.BooleanField(default=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        return self.company.name_en
    

class SystemSettings(models.Model):
    company = models.OneToOneField('company.Company', on_delete=models.PROTECT, unique=True, verbose_name=_("Company"), related_name='company')
    default_currency = models.CharField(max_length=3, choices=currency_choices, default='SAR')
    # Agent Settings
    agent_account_tree = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='agent_account_tree',verbose_name=_("Agent Account Tree"), null=True, blank=True)
    
    
    # Transport Company Settings
    transport_company_account_tree = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='transport_company_account_tree', verbose_name=_('Transport Company Account Tree') , null=True, blank=True)
    transport_expense_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='transport_expense_account', verbose_name=_('Transport Expense Account'), null=True, blank=True)

    # GIB Accounts
    gib_main_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='gib_main_account', verbose_name=_('GIB Main Account'), null=True, blank=True)
    gib_virtual_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='gib_virtual_account', verbose_name=_('GIB Virtual Account'), null=True, blank=True)

    # Settlement Account Settings
    settlement_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='settlement_account', verbose_name=_('Settlement Account'), null=True, blank=True)

    umrah_visa_purchase_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='umrah_visa_purchase_account', verbose_name=_('Umrah Visa Purchase Account'), null=True, blank=True)
    umrah_visa_sales_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='umrah_visa_sales_account', verbose_name=_('Umrah Visa Sales Account'), null=True, blank=True)

    transport_purchase_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='transport_purchase_account', verbose_name=_('Transport Purchase Account'), null=True, blank=True)
    transport_sales_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='transport_sales_account', verbose_name=_('Transport Sales Account'), null=True, blank=True)

    vat_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='vat_account', verbose_name=_('VAT Account'), null=True, blank=True)

    # Agent Commission Account Settings
    agent_commission_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, related_name='agent_commission_account', verbose_name=_('Agent Commission Account'), null=True, blank=True)

    account_statement_note = models.TextField(verbose_name=_('Account Statement Note'), null=True, blank=True)
    edit_hours = models.PositiveIntegerField(verbose_name=_("Edit Hours"), default=24)
    delete_hours = models.PositiveIntegerField(verbose_name=_("Delete Hours"), default=24)



    history = HistoricalRecords(
        user_model='auth.User',
    )

    def __str__(self):
        return self.company.name_en




