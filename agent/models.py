from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from .choices import *
from payment.models import AgentPaymentTransaction
from django.db.models import Avg, Count, Min, Sum
from .choices import agent_type
from voucher.models import AgentVoucher
from simple_history.models import HistoricalRecords
import secrets
import base64
import random, string
import company.models as company_models
from account.models import Account  
from django.core.exceptions import ObjectDoesNotExist
import datetime
from visa_group.models import UmrahVisaGroupInvoice

# Create your models here.




class Agent(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, verbose_name=_("Company"))
    country = models.ForeignKey("core.Country", on_delete=models.PROTECT , verbose_name=_("Country"))
    code = models.CharField(max_length=10, default="", verbose_name=_("Code"), blank=True, null=True)
    agent_type = models.CharField(verbose_name=_('Agent type'), max_length=16, choices=agent_type)
    name_en = models.CharField(max_length=64, verbose_name=_("Agent Name English"))
    name_ar = models.CharField(max_length=64, verbose_name=_("Agent Name Arabic"))


    address = models.TextField(verbose_name=_("Agent Address"), max_length=256)     
    contact = models.TextField(verbose_name=_("Agent contact"), max_length=256)

    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, verbose_name=_("User"), blank=True, null=True)
    token = models.CharField(max_length=64, verbose_name=_("Token"), blank=True, null=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )
    account = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name=_("Account"), blank=True, null=True, limit_choices_to={'level': 5, 'account_type': 'A'})

    can_view_account_statement = models.BooleanField(_("Can View Account Statement"), default=False)
    def save(self, *args, **kwargs):
        if self.account:
            account = Account.objects.get(pk=self.account.pk)
            account.account_name_en = self.name_en
            account.account_name_ar = self.name_ar
            account.allow_edit = False
            if self.agent_type == 'external':
                account.parent_account = company_models.SystemSettings.objects.get(company=self.company).external_agents_account
            else:
                account.parent_account = company_models.SystemSettings.objects.get(company=self.company).virtual_agents_account


            account.save()
        else:
            if self.agent_type == 'external':
                parent_account = company_models.SystemSettings.objects.get(company=self.company).external_agents_account
            else:
                parent_account = company_models.SystemSettings.objects.get(company=self.company).virtual_agents_account
            
            account = Account()
            account.company = self.company
            account.account_name_en = self.name_en
            account.account_name_ar = self.name_ar
            account.account_type = "A"
            account.level = 5
            account.parent_account = parent_account
            allow_edit = False
            account.save()
            print("Account Created")
            self.account = account
            self.save() 
        


        if self.user:
            if self.token:
                print("token available")
                
            else:
                print("token not available")
                self.token = (base64.b32encode(bytearray('umrahpro'+str(str(self.company.permit_no)+str(self.id)), 'ascii')).decode('utf-8')).replace('=', '')
        super(Agent, self).save(*args, **kwargs)

        # create AgentCommission object
        try:
            agent_commission = AgentCommission.objects.get(agent=self)
            
        except ObjectDoesNotExist:
            agent_commission = AgentCommission()
            agent_commission.agent = self
            agent_commission.company = self.company
            agent_commission.date = datetime.date.today()
            agent_commission.save()
        
        super(Agent, self).save(*args, **kwargs)




    def __str__(self):
        if get_language() == 'ar':
            return self.name_ar 
        return self.name_en 
    


    def name(self):
        if get_language() == 'ar':
            return self.name_ar
        return self.name_en
    
    def hidden_name(self):
        # Make a hidden name like A**** A****
        name = self.name()
        name = name.split(' ')
        hidden_name = ''
        for n in name:
            hidden_name += n[0] + '*'*(len(n)-1) + ' '
        return hidden_name.strip()
    


    def visa_sale_price(self):
        return self.sale_price
    
    def total_visas(self):
        t = UmrahVisaGroupInvoice.objects.filter(agent=self).aggregate(Sum('pax'))
        # return value without point 0.00
        if t['pax__sum'] is None:
            t = 0
        else:
            t = t['pax__sum']
        return t
    
    def current_visa_price(self):
        try:
            p = AgentPrice.objects.filter(agent=self).latest('date', 'pk')
            return p.visa_price
        except:
            return 0.00
    
    def current_visa_including_transport_price(self):
        try:
            p = AgentPrice.objects.filter(agent=self).latest('date', 'pk')
            return p.visa_included_transport_price
        except:
            return 0.00
        
    def transport_included_by_default(self):
        
        p = AgentPrice.objects.filter(agent=self).latest('date', 'pk').transport_included_by_default
        if p:
            print("Transport Included By Default")
        else:
            print("Transport Not Included By Default")

    
        
    def total_arrival_vouchers(self):
        from arrival_voucher.models import ArrivalVoucher

        t = ArrivalVoucher.objects.filter(agent=self).aggregate(Sum('pax'))
        # return value without point 0.00
        if t['pax__sum'] is None:
            t = 0
        else:
            t = t['pax__sum']
        return t
    
    def total_transport_pax(self):
        from arrival_voucher.models import ArrivalVoucher
        pax = ArrivalVoucher.objects.filter(agent=self, transport_type__show_in_transport_report=True).aggregate(Sum('pax'))
        if pax['pax__sum'] is None:
            pax = 0
        else:
            pax = pax['pax__sum']
        return pax
    def code_count(self):
        count = AgentCode.objects.filter(agent=self).count()
        return count
sub_agent_platform = (
    ('nusuk', _('Nusuk')),
    ('tawaf', _('Tawaf')),
    ('waytoumrah', _('Way to Umrah')),
    ('babalumrah', _('Baba Al Umrah')),
)

class AgentCode(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name=_("Agent"))
    platform = models.CharField(max_length=64, verbose_name=_("Platform"), choices = sub_agent_platform, default='nusuk')
    code = models.CharField(max_length=64, verbose_name=_("Code"), unique=True)
    country = models.ForeignKey("core.Country", on_delete=models.PROTECT , verbose_name=_("Country"))
    def __str__(self):
        return f"{self.agent.name()} - {self.get_platform_display()} "
    



class AgentPrice(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, verbose_name=_("Agent"))
    date = models.DateField(_("Change Date"), auto_now=False, auto_now_add=False)
    visa_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Visa Price"))
    visa_included_transport_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Visa Included Transport Price"))
    transport_included_by_default = models.BooleanField(_("Transport Included By Default"), default=False)

    changed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Changed By"), blank=True, null=True)

    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        return f"{self.agent.name()} - {self.date}"
    


class AgentCommission(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, verbose_name=_("Company"))
    agent = models.OneToOneField(Agent, on_delete=models.PROTECT, verbose_name=_("Agent"), related_name="commission")
    comission_holder_account = models.ForeignKey('account.Account', on_delete=models.PROTECT, verbose_name=_("Comission Holder Account"), blank=True, null=True)
    date = models.DateField(_("Change Date"), auto_now=False, auto_now_add=False)
    commission_per_visa_with_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Commission Per Visa With Transport"))
    commission_per_visa_without_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Commission Per Visa Without Transport"))
    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        return f"{self.agent.name()}"