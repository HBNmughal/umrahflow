from django.db import models

from account.models import Account, JournalEntry, Transaction
from django.utils.translation import gettext_lazy as _
from company.models import SystemSettings
# Create your models here.




class TransportPurchaseInvoice(models.Model):
    company = company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    transport_company = models.ForeignKey('transport.TransportCompany', on_delete=models.PROTECT, null=True, blank=True)
    arrival_voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.PROTECT)
    date = models.DateField(verbose_name=_("Date"))
    invoice_no = models.CharField(verbose_name=_("Invoice No"), max_length=256)
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Amount"))
    vat_percentage = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("VAT Percentage"), null=True, blank=True)
    vat_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("VAT Amount"), null=True, blank=True)
    transaction = models.ForeignKey('account.Transaction', on_delete=models.SET_NULL, blank=True, null=True)
    additional_movement = models.BooleanField(verbose_name=_("Additional Movement"), default=False, blank=True, null=True,)
    movement = models.ForeignKey('transport.TransportMovement', on_delete=models.SET_NULL, blank=True, null=True, related_name='additional_movement')
    supplier_entry = models.ForeignKey('account.JournalEntry', on_delete=models.SET_NULL, blank=True, null=True, related_name='supplier_entry', verbose_name=_("Supplier Entry"),editable=False)
    expense_entry = models.ForeignKey('account.JournalEntry', on_delete=models.SET_NULL, blank=True, null=True, related_name='expense_entry', verbose_name=_("Expense Entry"),editable=False)


    class Meta:
        verbose_name = _("Transport Purchase Invoice")
        verbose_name_plural = _("Transport Purchase Invoices")
    def __str__(self):
        if self.arrival_voucher:
            return f"{self.arrival_voucher}"
    def save(self, *args, **kwargs):
        from transport.models import TransportMovement

        super().save(*args, **kwargs)
        if not self.transaction:
            transaction = Transaction()
            transaction.company = self.company
            transaction.date = self.date
            if self.additional_movement:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + ", Voucher no. UP-" + str(self.arrival_voucher.pk) +", Additional Movement: " + str(self.movement.route.name_en())
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "، رقم البرنامج UP-" + str(self.arrival_voucher.pk) + " حركة إضافية: " + str(self.movement.route.name_ar())
            else:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + "Voucher no. UP-" + str(self.arrival_voucher.pk) 
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "رقم البرنامج UP-" + str(self.arrival_voucher.pk)

            transaction.save()
            self.transaction = transaction
            supplier_entry = JournalEntry()
            supplier_entry.company = self.company
            supplier_entry.date = self.date
            supplier_entry.transaction = transaction
            supplier_entry.account = self.transport_company.account
            supplier_entry.debit = self.amount
            supplier_entry.credit = 0.00
            supplier_entry.save()
            self.supplier_entry = supplier_entry
            expense_entry = JournalEntry()
            expense_entry.company = self.company
            expense_entry.date = self.date
            expense_entry.transaction = transaction
            expense_entry.account = SystemSettings.objects.get(company=self.company).transport_expense_account
            expense_entry.debit = 0.00
            expense_entry.credit = self.amount
            expense_entry.save()
            self.expense_entry = expense_entry
            transaction.save()
            super().save(*args, **kwargs)

            if self.additional_movement:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + ", Voucher no. UP-" + str(self.arrival_voucher.pk) +", Additional Movement: " + str(self.movement.route.name_en())
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "، رقم البرنامج UP-" + str(self.arrival_voucher.pk) + " حركة إضافية: " + str(self.movement.route.name_ar())
            else:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + "Voucher no. UP-" + str(self.arrival_voucher.pk)
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "رقم البرنامج UP-" + str(self.arrival_voucher.pk)
            transaction.save()
            super().save(*args, **kwargs)


            
            

        else:
            transaction = Transaction.objects.get(pk=self.transaction.pk)
            transaction.company = self.company
            transaction.date = self.date
            if self.additional_movement:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + ", Voucher no. UP-" + str(self.arrival_voucher.pk) +", Additional Movement: " + str(self.movement.route.name_en())
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "، رقم البرنامج UP-" + str(self.arrival_voucher.pk) + " حركة إضافية: " + str(self.movement.route.name_ar())
            else:
                transaction.description_en = "Transport Invoice, " + self.invoice_no + "Voucher no. UP-" + str(self.arrival_voucher.pk)
                transaction.description_ar = "فاتورة النقل " + self.invoice_no + "رقم البرنامج UP-" + str(self.arrival_voucher.pk)
            transaction.save()
            self.transaction = transaction
            supplier_entry = JournalEntry.objects.get(pk=self.supplier_entry.pk)
            supplier_entry.company = self.company
            supplier_entry.date = self.date
            supplier_entry.transaction = transaction
            supplier_entry.account = self.transport_company.account
            supplier_entry.debit = self.amount
            supplier_entry.credit = 0.00
            supplier_entry.save()
            self.supplier_entry = supplier_entry
            expense_entry = JournalEntry.objects.get(pk=self.expense_entry.pk)
            expense_entry.company = self.company
            expense_entry.date = self.date
            expense_entry.transaction = transaction
            expense_entry.account = SystemSettings.objects.get(company=self.company).transport_expense_account
            expense_entry.debit = 0.00
            expense_entry.credit = self.amount
            expense_entry.save()
            self.expense_entry = expense_entry
            
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction:
            self.transaction.delete()
        super().delete(*args, **kwargs)

        


# class GroupVoucher(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
#     agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT)
#     date = models.DateField(verbose_name=_("Date"))
#     group_no = models.CharField(verbose_name=_("Group No"), max_length=256)
#     voucher_no = models.CharField(verbose_name=_("Voucher No"), max_length=256)
#     pax = models.IntegerField(verbose_name=_("Pax"), min=0)


#     # Purchase
#     purchase_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Purchase Amount"), min=0.00)
#     purchase_vat_percentage = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Purchase VAT Percentage"), null=True, blank=True, min=0.00)
    

#     sale_price = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Sale Price"), min=0.00)
#     vat_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("VAT Amount"), null=True, blank=True, min=0.00)
#     included_transport = models.BooleanField(verbose_name=_("Included Transport"), default=False, blank=True, null=True, )


#     # Transaction
#     transaction = models.ForeignKey('account.Transaction', on_delete=models.SET_NULL, blank=True, null=True)
#     expense_entry = models.ForeignKey('account.JournalEntry', on_delete=models.SET_NULL, blank=True, null=True, related_name='expense_entry', verbose_name=_("Expense Entry"),editable=False)
#     client_entry = models.ForeignKey('account.JournalEntry', on_delete=models.SET_NULL, blank=True, null=True, related_name='client_entry', verbose_name=_("Client Entry"),editable=False)
    