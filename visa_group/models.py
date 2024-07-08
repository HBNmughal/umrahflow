from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from umrahflow.settings import VAT_PERCENTAGE
from core.utils import calculate_tax
from account.models import Transaction
from simple_history.models import HistoricalRecords
from decimal import Decimal

# Create your models here.






class UmrahVisaGroupInvoice(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name=_('Company'))
    date = models.DateField(default=timezone.now, verbose_name=_('Issue Date'))
    agent = models.ForeignKey('agent.Agent', on_delete=models.CASCADE, verbose_name=_('Agent'))
    group_no = models.CharField(max_length=50, verbose_name=_('Group No'), unique=True)
    voucher_no = models.CharField(max_length=50, verbose_name=_('Voucher No'), unique=True)
    pax = models.IntegerField(verbose_name=_('PAX'), default=1)
    visa_sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Visa Price'))
    transport_included = models.BooleanField(default=False, verbose_name=_('Transport Included'))
    comission_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Comission Rate'))

    vat_percentage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('VAT Percentage'), default=VAT_PERCENTAGE)

    ground_service_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Ground Service Price'), default=0.00)
    visa_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Visa Fee'), default=300.00)
    insurance_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Insurance Fee'), default=64.85)
    electronic_services_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Electronic Services Fee'), default=102.07)


    transport_brn = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Transport BRN'), default=1.00)
    hotel_brn = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Hotel BRN'), default=1.00)
    
    transaction = models.ForeignKey('account.Transaction', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Transaction'))


    history = HistoricalRecords(
        user_model='auth.User',
    )




    def __str__(self):
        return self.group_no
    
    def total_visa_price(self):
        return self.visa_sale_price * self.pax
    
    def total_comission(self):
        try:
            rate_transport_included = self.agent.commission.commission_per_visa_with_transport
            rate_without_transport = self.agent.commission.commission_per_visa_without_transport
            if self.transport_included:
                return rate_transport_included * self.pax
                
            else:
                return rate_without_transport * self.pax
        except:
            return Decimal(0.00)
        
    def paid_amount_in_bank(self):
        general_fees = (self.visa_fees + self.insurance_fees + self.electronic_services_fees) * self.pax
        brn = self.transport_brn  + self.hotel_brn 
        ground_services = self.ground_service_price * self.pax

        return general_fees + brn + ground_services


    def amount_paid_in_bank(self):
        general_fees = (self.visa_fees + self.insurance_fees + self.electronic_services_fees) * self.pax
        brn = self.transport_brn  + self.hotel_brn
        ground_services = self.ground_service_price * self.pax
        return general_fees + brn + ground_services


    def total_sale_amount(self):
        general_fees = (self.visa_fees + self.insurance_fees + self.electronic_services_fees) * self.pax #467.92
        brn = self.transport_brn  + self.hotel_brn 
        visa_price = self.visa_sale_price * self.pax #600

        sale_amount = visa_price - general_fees # 132.08
 
        return sale_amount
    
    def sale_vat(self):
        print(f"Total Sale Amount: {self.total_sale_amount()}")
        print(f"VAT Percentage: {self.vat_percentage}")
        print(calculate_tax(self.total_sale_amount(), self.vat_percentage))
        return calculate_tax(self.total_sale_amount(), self.vat_percentage)
    
    def total_sale_amount_without_vat(self):
        return self.total_sale_amount() - self.sale_vat()
    
    def bank_refund_amount(self):
        # Bank Refund is the amount of BRN of hotel and transport + ground services
        return self.transport_brn + self.hotel_brn + self.ground_service_price * self.pax

    def external_agent_entry(self):
        amount = self.amount_paid_in_bank() - self.total_visa_price()
        if amount > 0.00:
            print('Amount is greater than 0 and will be credited to agent account')
            print(f'Amount: {abs(amount)}')
            entry = {
                'account': self.agent.account.pk,
                'transaction_type': 'credit',
                'amount': abs(amount),
                'entry_for': 'visa_sale_agent'
            },
            return entry
        elif amount < 0.00:
            print('Amount is less than 0 and will be debited from agent account')
            print(f'Amount: {abs(amount)}')
            entry = {
                'account': self.agent.account.pk,
                'transaction_type': 'debit',
                'amount': abs(amount),
                'entry_for': 'visa_sale_agent'
            },
            return entry

    


    def save(self, *args, **kwargs):

        print(f"Total Visa Price: {self.total_visa_price()}")
        print(f"GIB Virtual Account Entry: {self.amount_paid_in_bank()}")
        print(f"GIB Refund Entry: {self.bank_refund_amount()}")
        print(f"Revenue Entry: {self.total_sale_amount_without_vat() - self.total_comission()}")
        print(f"Comission Entry: {self.total_comission()}")
        print(f"VAT Entry: {self.sale_vat()}")
        
        # Sale Transaction
        # Virtual Agent (In Case) company paid amount from its own account
        if self.agent.agent_type == 'virtual':
            print('Creating Transaction for Virtual Agent')
            try:
                if self.comission_rate == 0.00 or self.comission_rate is None:
                    self.comission_rate = (self.agent.commission.commission_per_visa_with_transport if self.transport_included else self.agent.commission.commission_per_visa_without_transport)
            except:
                self.comission_rate = 0.00
            if self.pk is None:
                visa_sale_transaction = Transaction.objects.create_transaction_with_entries(
                company=self.company,
                description_en= f'Visa Group Invoice {self.group_no}',
                description_ar= f'فاتورة مجموعة تأشيرات {self.group_no}',
                reference_no= self.group_no,
                ledger_entries=[
                    # Debit Entry for Agent Account
                    {
                    'account': self.agent.account.pk,
                    'transaction_type': 'debit',
                    'amount': self.total_visa_price(),
                    'entry_for': 'visa_sale_agent'
                    
                    },
                    # GIB Virtual Account Entry
                    {
                    'account': self.company.settings().gib_virtual_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.amount_paid_in_bank(),
                    'entry_for': 'gib_virtual_account_credit'
                    },
                    # GIB Refund Entry
                    {
                    'account': self.company.settings().gib_main_account.pk,
                    'transaction_type': 'debit',
                    'amount': self.bank_refund_amount(),
                    'entry_for': 'gib_refund'
                    },

                    # Revenue Entry
                    {
                    'account': self.company.settings().umrah_visa_sales_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.total_sale_amount_without_vat() - self.total_comission(),
                    'entry_for': 'visa_sale_revenue'

                    },
                    # Comission Entry
                    {
                    'account': self.agent.commission.comission_holder_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.total_comission(),
                    'entry_for': 'visa_sale_comission'
                    } if self.comission_rate > 0.00 else None,
                    # VAT Entry
                    {
                    'account': self.company.settings().vat_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.sale_vat(),
                    'entry_for': 'visa_sale_vat'
                    },

                ]

                )
            
                self.transaction = visa_sale_transaction
            else:
                # Update Transaction
                visa_sale_transaction = self.transaction
                visa_sale_transaction.description_en = f'Visa Group Invoice {self.group_no}'
                visa_sale_transaction.description_ar = f'فاتورة مجموعة تأشيرات {self.group_no}'
                visa_sale_transaction.reference_no = self.group_no
                visa_sale_transaction.save()

                # Update Ledger Entries
                # Debit Entry for Agent Account
                debit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_agent')
                debit_entry.debit = self.total_visa_price()
                debit_entry.save()

                # GIB Virtual Account Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='gib_virtual_account_credit')
                credit_entry.credit = self.amount_paid_in_bank()
                credit_entry.save()

                # GIB Refund Entry
                debit_entry = visa_sale_transaction.entries.get(entry_for='gib_refund')
                debit_entry.debit = self.bank_refund_amount()
                debit_entry.save()

                # Revenue Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_revenue')
                credit_entry.credit = self.total_sale_amount_without_vat() - self.total_comission()
                credit_entry.save()

                # Comission Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_comission')
                credit_entry.credit = self.total_comission()
                credit_entry.save()

                # VAT Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_vat')
                credit_entry.credit = self.sale_vat()
                credit_entry.save()
        elif self.agent.agent_type == 'external':
            try:
                if self.comission_rate == 0.00 or self.comission_rate is None:
                    self.comission_rate = (self.agent.commission.commission_per_visa_with_transport if self.transport_included else self.agent.commission.commission_per_visa_without_transport) if self.agent.commission else 0.00
            except:
                self.comission_rate = 0.00

            if self.pk is None:
                visa_sale_transaction = Transaction.objects.create_transaction_with_entries(
                company=self.company,
                description_en= f'Visa Group Invoice {self.group_no}',
                description_ar= f'فاتورة مجموعة تأشيرات {self.group_no}',
                reference_no= self.group_no,
                ledger_entries=[
                    # Entry for Agent Account
                    {
                        'account': self.agent.account.pk,
                        'transaction_type': 'credit' if self.amount_paid_in_bank() - self.total_visa_price() > 0.00 else 'debit',
                        'amount': abs(self.amount_paid_in_bank() - self.total_visa_price()),
                        'entry_for': 'visa_sale_agent'
                    },

                    # GIB Virtual Account Entry
                    {
                        'account': self.company.settings().gib_main_account.pk,
                        'transaction_type': 'debit',
                        'amount': self.bank_refund_amount(),
                        'entry_for': 'gib_refund'
                    },
                    # Revenue Entry
                    {
                    'account': self.company.settings().umrah_visa_sales_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.total_sale_amount_without_vat() - self.total_comission(),
                    'entry_for': 'visa_sale_revenue'

                    },
                    # Comission Entry
                    {
                    'account': self.agent.commission.comission_holder_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.total_comission(),
                    'entry_for': 'visa_sale_comission'
                    } if self.comission_rate > 0.00 else None,
                    # VAT Entry
                    {
                    'account': self.company.settings().vat_account.pk,
                    'transaction_type': 'credit',
                    'amount': self.sale_vat(),
                    'entry_for': 'visa_sale_vat'
                    },
                ]
                    
                )
                self.transaction = visa_sale_transaction
            else:
                # Update Transaction
                visa_sale_transaction = self.transaction
                visa_sale_transaction.description_en = f'Visa Group Invoice {self.group_no}'
                visa_sale_transaction.description_ar = f'فاتورة مجموعة تأشيرات {self.group_no}'
                visa_sale_transaction.reference_no = self.group_no
                visa_sale_transaction.save()

                # Update Ledger Entries
                # Entry for Agent Account
                entry = visa_sale_transaction.entries.get(entry_for='visa_sale_agent')
                entry.account = self.agent.account
                entry.debit = abs(self.amount_paid_in_bank() - self.total_visa_price()) if self.amount_paid_in_bank() - self.total_visa_price() < 0.00 else 0.00
                entry.credit = abs(self.amount_paid_in_bank() - self.total_visa_price()) if self.amount_paid_in_bank() - self.total_visa_price() > 0.00 else 0.00

                entry.save()

                # GIB Refund Entry
                debit_entry = visa_sale_transaction.entries.get(entry_for   ='gib_refund')
                debit_entry.debit = self.bank_refund_amount()
                debit_entry.save()

                # Revenue Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_revenue')
                credit_entry.credit = self.total_sale_amount_without_vat() - self.total_comission()
                credit_entry.save()

                if self.comission_rate > 0.00:
                    # Comission Entry
                    credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_comission')
                    credit_entry.credit = self.total_comission()
                    credit_entry.save()
                else:
                    try:
                        visa_sale_transaction.entries.get(entry_for='visa_sale_comission').delete()
                    except:
                        pass


                # VAT Entry
                credit_entry = visa_sale_transaction.entries.get(entry_for='visa_sale_vat')
                credit_entry.credit = self.sale_vat()
                credit_entry.save()
        else:
            print('Agent Type is not defined')


        super(UmrahVisaGroupInvoice, self).save(*args, **kwargs)



        
class UmrahVisaGroupInvoiceDefaultPrices(models.Model):
    company = models.OneToOneField('company.Company', on_delete=models.CASCADE, verbose_name=_('Company'))
    ground_service_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Ground Service Price'), default=0.00)
    visa_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Visa Fee'), default=300.00)
    insurance_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Insurance Fee'), default=64.85)
    electronic_services_fees = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Electronic Services Fee'), default=102.07)
    transport_brn = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Transport BRN'), default=1.00)
    hotel_brn = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Hotel BRN'), default=1.00)

    history = HistoricalRecords(
        user_model='auth.User',
    )


    def __str__(self):
        return str(self.company)
