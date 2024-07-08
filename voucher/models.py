from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
import math
from decimal import Decimal
from django.db.models import F, Sum
from payment.models import AgentPaymentTransaction
from django.core.exceptions import ObjectDoesNotExist
import datetime
from simple_history.models import HistoricalRecords
from account.models import Transaction, JournalEntry
# Create your models here.


class AgentVoucher(models.Model):
    company = models.ForeignKey("company.Company", on_delete=models.PROTECT ,verbose_name=_("Company"))
    agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT,verbose_name=_("Agent"))
    voucher_no = models.CharField( max_length=7, unique=True,verbose_name=_("Voucher no"))
    group_id = models.IntegerField(verbose_name=_("Group ID"), null= True, blank=True)
    pax = models.IntegerField(verbose_name=_("PAX"))
    amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Amount"),default=0.00)
    date = models.DateTimeField(verbose_name=_("Voucher Date and Time"))
    arrival_date = models.DateField(verbose_name=_("Arrival Date"), null=True, blank=True)
    group_no = models.CharField(max_length=10,verbose_name=_("Group no"))
    group_name = models.CharField(max_length=64,verbose_name=_("Group Name"), null= True, blank=True)
    account_no = models.CharField(max_length=64, verbose_name=_("Account No."), null= True, blank=True)
    extra_fees = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Extra Fees"), null= True, blank=True, default=0.00)
    voucher_expiry = models.DateTimeField(verbose_name=_("Voucher Expiry"), null= True, blank=True)
    ground_services_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Ground Services Price"), null= True, blank=True, default=0.00)
    additional_services_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Additional Services Price"), null= True, blank=True, default=0.00)
    processing_fees = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Processing Fees"), null= True, blank=True, default=0.00)
    visa_fees = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Visa Fees"), null= True, blank=True)
    insurance_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Insurance Fees"), null= True, blank=True, default=0.00)
    transport_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Transport BRN Price"), null= True, blank=True, default=0.00)
    makkah_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Makkah BRN Price"), null= True, blank=True, default=0.00)
    medina_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Medina BRN Price"), null= True, blank=True, default=0.00)
    sale_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Sale Price"), null= True, blank=True, default=0.00)

    #Returns
    transport_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Transport BRN Return"), null= True, blank=True, default=0.00)
    makkah_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Makkah BRN Return"), null= True, blank=True, default=0.00)
    medina_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Medina BRN Return"), null= True, blank=True, default=0.00)
    ground_services_price_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Ground Services Fee Return"), null= True, blank=True, default=0.00)
    vat_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("VAT Return"), null= True, blank=True, default=0.00)
    commission = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Commission"), null= True, blank=True, default=0.00)
    agent_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Refund Agent"), null= True, blank=True, default=0.00)
    # transaction = models.ForeignKey('account.Transaction', on_delete=models.PROTECT,verbose_name=_("Transaction"), null= True, blank=True)
    # purchase_entry = models.ForeignKey('account.JournalEntry',related_name="purchase_entry",  on_delete=models.PROTECT,verbose_name=_("Purchase"), null= True, blank=True)
    # sale_entry = models.ForeignKey('account.JournalEntry',related_name="sale_entry", on_delete=models.PROTECT,verbose_name=_("Sale"), null= True, blank=True)

    purchase_transaction = models.ForeignKey('account.Transaction', on_delete=models.PROTECT,verbose_name=_("Purchase Transaction"), null= True, blank=True, related_name='purchase_transaction')
    purchase_credit_entry = models.ForeignKey('account.JournalEntry',related_name="purchase_credit_entry",  on_delete=models.PROTECT,verbose_name=_("Purchase Credit Entry"), null= True, blank=True)
    purchase_debit_entry = models.ForeignKey('account.JournalEntry',related_name="purchase_debit_entry",  on_delete=models.PROTECT,verbose_name=_("Purchase Debit Entry"), null= True, blank=True)

    sale_transaction = models.ForeignKey('account.Transaction', on_delete=models.PROTECT,verbose_name=_("Sale Transaction"), null= True, blank=True, related_name='sale_transaction')
    sale_credit_entry = models.ForeignKey('account.JournalEntry',related_name="sale_credit_entry",  on_delete=models.PROTECT,verbose_name=_("Sale Credit Entry"), null= True, blank=True)
    sale_debit_entry = models.ForeignKey('account.JournalEntry',related_name="sale_debit_entry",  on_delete=models.PROTECT,verbose_name=_("Sale Debit Entry"), null= True, blank=True)
    



    history = HistoricalRecords(
        user_model='auth.User',
    )


    class Meta:
        permissions = [
            ("can_view_visa_invoice", _("Can view visa invoice")),
            ("can_edit_visa_invoice", _("Can edit visa invoice")),
            ("can_delete_visa_invoice", _("Can delete visa invoice")),
            ('can_view_transport_invoice', _('Can view transport invoice')),
        ]



    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        from account.models import Transaction, JournalEntry
        from company.models import Company, SystemSettings
        
        if self.purchase_transaction:
            transaction = self.purchase_transaction
            transaction.company = self.company
            transaction.date = self.date
            transaction.description_ar = "فاتورة تأشيرات عمرة، رقم الفاتورة: " + str(self.voucher_no) + "، السعر: " + str(self.sale_price) + "، عدد التاشيرات: " + str(self.pax) + "، رقم المجموعة: " + self.group_no
            transaction.description_en = "Umrah Visas Voucher, Voucher No: " + str(self.voucher_no) + ", Price: " + str(self.sale_price) + ", PAX: " + str(self.pax) + ", Group No: " + str(self.group_no)
            transaction.save()
            self.purchase_transaction = transaction
            # After Creating Transaction, Create JournalEntry for Purchase
            purchase_credit_entry = self.purchase_credit_entry
            purchase_credit_entry.company = self.company
            purchase_credit_entry.account = self.company.settings().umrah_visa_purchase_account
            purchase_credit_entry.transaction = self.purchase_transaction
            purchase_credit_entry.date = transaction.date
            purchase_credit_entry.credit =  float(self.sale_price) * int(self.pax)
            purchase_credit_entry.save()

            purchase_debit_entry = self.purchase_debit_entry
            purchase_debit_entry.company = self.company
            purchase_debit_entry.account = self.company.settings().umrah_visa_purchase_account
            purchase_debit_entry.transaction = self.purchase_transaction
            purchase_debit_entry.date = transaction.date
            purchase_debit_entry.debit = float(self.sale_price) * int(self.pax)
            purchase_debit_entry.save()
            super().save(*args, **kwargs)

        else:
            # First create Transaction
            journal_entries = [
                {
                    'account': self.company.settings().umrah_visa_purchase_account.id,
                    'transaction_type': 'credit',
                    'amount': float(self.sale_price) * int(self.pax)
                },
                {
                    'account': self.company.settings().umrah_visa_purchase_account.id,
                    'transaction_type': 'debit',
                    'amount': float(self.sale_price) * int(self.pax)
                }
            ]

            transaction = Transaction.objects.create_transaction_with_entries(
                company=self.company,
                description_en="Umrah Visas Voucher, Voucher No: " + str(self.voucher_no) + ", Price: " + str(self.sale_price) + ", PAX: " + str(self.pax) + ", Group No: " + str(self.group_no),
                description_ar="فاتورة تأشيرات عمرة، رقم الفاتورة: " + str(self.voucher_no) + "، السعر: " + str(self.sale_price) + "، عدد التاشيرات: " + str(self.pax) + "، رقم المجموعة: " + self.group_no,
                reference_no=self.voucher_no,
                ledger_entries=journal_entries
            )
            self.purchase_transaction = transaction
            super().save(*args, **kwargs)

        
        if self.sale_transaction:
            transaction = self.sale_transaction
            transaction.company = self.company
            transaction.date = self.date
            transaction.description_ar = "فاتورة تأشيرات عمرة، رقم الفاتورة: " + str(self.voucher_no) + "، السعر: " + str(self.sale_price) + "، عدد التاشيرات: " + str(self.pax) + "، رقم المجموعة: " + self.group_no
            transaction.description_en = "Umrah Visas Voucher, Voucher No: " + str(self.voucher_no) + ", Price: " + str(self.sale_price) + ", PAX: " + str(self.pax) + ", Group No: " + str(self.group_no)
            transaction.save()
            self.sale_transaction = transaction
            # After Creating Transaction, Create JournalEntry for Sale
            sale_credit_entry = self.sale_credit_entry
            sale_credit_entry.company = self.company
            sale_credit_entry.account = self.company.settings().umrah_visa_sale_account
            sale_credit_entry.transaction = self.sale_transaction
            sale_credit_entry.date = transaction.date
            sale_credit_entry.credit =  float(self.sale_price) * int(self.pax)
            sale_credit_entry.save()

            sale_debit_entry = self.sale_debit_entry
            sale_debit_entry.company = self.company
            sale_debit_entry.account = self.company.settings().umrah_visa_sale_account
            sale_debit_entry.transaction = self.sale_transaction
            sale_debit_entry.date = transaction.date
            sale_debit_entry.debit = float(self.sale_price) * int(self.pax)
            sale_debit_entry.save()
            super().save(*args, **kwargs)
        
        else:
            # First create Transaction
            journal_entries = [
                {
                    'account': self.company.settings().umrah_visa_sale_account.id,
                    'transaction_type': 'credit',
                    'amount': float(self.sale_price) * int(self.pax)
                },
                {
                    'account': self.company.settings().umrah_visa_sale_account.id,
                    'transaction_type': 'debit',
                    'amount': float(self.sale_price) * int(self.pax)
                }
            ]

            transaction = Transaction.objects.create_transaction_with_entries(
                company=self.company,
                description_en="Umrah Visas Voucher, Voucher No: " + str(self.voucher_no) + ", Price: " + str(self.sale_price) + ", PAX: " + str(self.pax) + ", Group No: " + str(self.group_no),
                description_ar="فاتورة تأشيرات عمرة، رقم الفاتورة: " + str(self.voucher_no) + "، السعر: " + str(self.sale_price) + "، عدد التاشيرات: " + str(self.pax) + "، رقم المجموعة: " + self.group_no,
                reference_no=self.voucher_no,
                ledger_entries=journal_entries
            )
            self.sale_transaction = transaction
            super().save(*args, **kwargs)
            
        

    def delete(self, *args, **kwargs):
        from account.models import Transaction, JournalEntry
        try:
            transaction = self.purchase_transaction
            transaction.delete()
        except:
            pass
        try:
            purchase_credit_entry = self.purchase_credit_entry
            purchase_credit_entry.delete()
        except:
            pass
        try:
            purchase_debit_entry = self.purchase_debit_entry
            purchase_debit_entry.delete()
        except:
            pass
        try:
            transaction = self.sale_transaction
            transaction.delete()
        except:
            pass
        try:
            sale_credit_entry = self.sale_credit_entry
            sale_credit_entry.delete()
        except:
            pass
        try:
            sale_debit_entry = self.sale_debit_entry
            sale_debit_entry.delete()
        except:
            pass
        super().delete(*args, **kwargs)
        



    
    def __str__(self):
        return self.voucher_no

    def _amount(self):
        sub_total = self.ground_services_price + self.processing_fees + self.visa_fees + self.insurance_price * self.pax
        total = sub_total + self.transport_brn_price + self.makkah_brn_price + self.medina_brn_price
        return round(total, 2)



    def voucher_total(self):
        total = {}
        total["transport_brn_return"] = round(self.transport_brn_return * self.pax, 2)
        total['makkah_brn_return'] = round(self.makkah_brn_return * self.pax, 2)
        total['medina_brn_return'] = round(self.medina_brn_return * self.pax, 2)
        total['sale_price'] = round(self.sale_price * self.pax, 2)
        total['vat_return'] = round(self.vat_return * self.pax, 2)
        total['ground_services_price_return'] = round(self.ground_services_price_return * self.pax, 2)
        total['agent_return'] = round(self.agent_return * self.pax, 2) 
        total['commission'] = round(self.commission * self.pax, 2) 

      
        total['returns'] = round(
            total["transport_brn_return"] +
            total['makkah_brn_return'] +
            total['medina_brn_return'] +
            total['ground_services_price_return'] 
        ,2)

        total_1 = round(
            self.amount -
            total['returns']
            ,2)
        total['profit'] = round(
            total['sale_price'] -
            total_1 - total['commission']
            , 2)

        return total
    
    def total(self):
        return round(self.sale_price * self.pax, 2)
        

    
    








class FixedVoucherPrices(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    ground_services_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Ground Services Price"))
    additional_services_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Additional Services Price"))
    processing_fees = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Processing Fees"))
    visa_fees = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Visa Fees"))
    insurance_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Insurance Fees"))
    transport_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Transport BRN Price"), null= True, blank=True, default=0.00)
    makkah_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Makkah BRN Price"), null= True, blank=True, default=0.00)
    medina_brn_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Medina BRN Price"), null= True, blank=True, default=0.00)
    sale_price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Sale Price"), null= True, blank=True, default=0.00)
    transport_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Transport BRN Return"), null= True, blank=True, default=0.00)
    makkah_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Makkah BRN Return"), null= True, blank=True, default=0.00)
    medina_brn_return = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Medina BRN Return"), null= True, blank=True, default=0.00)
    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        fees = [self.ground_services_price, self.additional_services_price,self.processing_fees,self.visa_fees,self.insurance_price]
        return str(math.fsum(fees))
    




class PurchaseInvoice(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT)
    invoice_no = models.CharField(max_length=255,verbose_name=_("Invoice No"))
    item = models.CharField(max_length=255,verbose_name=_("Item"))
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    date = models.DateField(verbose_name=_("Date"))
    total_cost = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Total Cost"), null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Tax Percentage"), null=True, blank=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )

    def tax_amount(self):
        return round(self.total_cost * self.tax_percentage / 100, 2)
    


TRANSPORT_TYPE = (
    ('bus', _('Bus')),
    ('shared', _('Shared Bus')),
    ('private_car', _('Private Car')),
)




class TransportInvoice(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT   , verbose_name=_("Agent"))
    date = models.DateField(verbose_name=_("Date"),default=datetime.date.today)
    # voucher = models.ForeignKey('Voucher', on_delete=models.PROTECT, null=True, blank=True)
    purchase_invoice = models.ForeignKey('PurchaseInvoice', on_delete=models.PROTECT, null=True, blank=True)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT, null=True, blank=True)
    transport_type = models.ForeignKey('transport.TransportType', on_delete=models.PROTECT, null=True, blank=True)

    qty = models.IntegerField(verbose_name=_("Quantity"), db_column='qty', default=1)
    price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Price"))
    tax_percentage = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Tax Percentage"), null=True, blank=True)
    description = models.CharField(max_length=255,verbose_name=_("Description"), null=True, blank=True)
    arrival_voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.PROTECT, null=True, blank=True)
    referance_no = models.CharField(max_length=255,verbose_name=_("Reference No"), null=True, blank=True)
    additional_movement = models.BooleanField(verbose_name=_("Additional Movement"), default=False, blank=True, null=True, )
    movement = models.ForeignKey('transport.TransportMovement', on_delete=models.SET_NULL, blank=True, null=True, related_name='movement')
    allow_edit_manualy = models.BooleanField(verbose_name=_("Allow Edit Manualy"), default=True, blank=True, null=True, )
    
    

    # agent payment transaction
    agent_payment_transaction = models.ForeignKey('payment.AgentPaymentTransaction', on_delete=models.PROTECT, null=True, blank=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )

    

    def __str__(self):
        return str(self.date)
    
    def total(self):
        return round(self.price * self.qty, 2)
    
    def save(self, *args, **kwargs):
        self.tax_percentage = 15
        # calculate tax from tax invluded amount    
        self.tax_amount = round((self.qty * self.price) / 100)
        super().save(*args, **kwargs)
        try:
            payment_transaction = AgentPaymentTransaction.objects.get(transport_invoice=self.id, transaction_type='d')
            payment_transaction.amount = self.total()
            payment_transaction.agent = self.agent
            payment_transaction.date = self.date
            payment_transaction.save()
        except ObjectDoesNotExist:
            new_payment_transaction = AgentPaymentTransaction()
            new_payment_transaction.company = self.company
            new_payment_transaction.agent = self.agent
            new_payment_transaction.amount = self.total()
            new_payment_transaction.transaction_type = 'd'
            new_payment_transaction.reason = _("Transport Invoice. Invoice No: " + str(self.id) + "Qty: " + str(self.qty) + "Price: " + str(self.price))
            new_payment_transaction.date = self.date
            new_payment_transaction.performed_by = ('System')
            new_payment_transaction.transport_invoice = self
            new_payment_transaction.save()

    def delete(self, *args, **kwargs):
        try:
            transaction = AgentPaymentTransaction.objects.get(transport_invoice=self)
            transaction.delete()
        except:
            pass
        super().delete(*args, **kwargs)

        