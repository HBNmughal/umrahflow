from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from threading import Timer
from django.utils import timezone
from django.utils.translation import get_language
from simple_history.models import HistoricalRecords



payment_by = (
    ("c", _("Cash")),
    ("b", _("Bank Account Transfer")),
)
transaction_type = (
    ("c", _("Credit")),
    ("d", _("Debit")),
    ("r", _("Refund")),
    ("rd", _("Refund Withdraw")),
    ("co", _("Commission")),
    ("cod", _("Commission Withdraw")),


)

wallet_transaction_type = (
    ("c", _("Credit")),
    ("d", _("Debit")),



)


reasons = (
    ("1", _("Visa Fees")),
    ("2", _("Transport Fees")),
    ("3", _("Accommodation Fees")),
    ("4", _("Fine / Violation Fees")),
    ("5", _("Catering Service Fees")),


)

salary_collection_status = (
    ("pending" , _("Pending")),
    ("collected" , _("Collected")),


)

treasury_payment_types = (
    ("general", _("General")),
    ("company_expense", _("Company Expense")),
    ("salary", _("Salary")),
    ("other", _("Other")),
)



class AgentPaymentTransaction(models.Model):
    company = models.ForeignKey("company.Company", verbose_name="Company", on_delete=models.PROTECT)
    agent = models.ForeignKey('agent.Agent', verbose_name="Agent", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Amount"))
    credit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Credit"), default=0.00)
    debit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Debit"), default=0.00)
    transaction_type = models.CharField(max_length=16, verbose_name="Transaction Type", choices=transaction_type)
    reason = models.CharField(max_length=64, verbose_name=_("Payment Type"), choices=reasons)
    payment_for = models.CharField(max_length=64, verbose_name=_("Payment For"))
    manual_receipt_no = models.CharField(max_length=16, verbose_name=_("Manual Receipt No."), null=True, blank=True)
    payment_by = models.CharField(max_length=16, verbose_name=_("Paid by"), choices=payment_by, null=True, blank=True, default="")
    date= models.DateField(_("Date"))
    time= models.TimeField(_("Time"), auto_now=True)
    performed_by = models.CharField(max_length=64, verbose_name=_("Performed By"))
    voucher = models.ForeignKey('voucher.AgentVoucher', on_delete=models.CASCADE, blank=True, null=True)
    transport_invoice = models.ForeignKey('voucher.TransportInvoice', on_delete=models.CASCADE, blank=True, null=True)
    received_by = models.CharField(max_length=64, verbose_name=_("Received By"), blank=True, null=True)
    is_settlement_transaction = models.BooleanField(default=False)
    history = HistoricalRecords(
        user_model='auth.User',
    )


    
    
    # This field is to store the transaction in account if account is selected
    # received_to_account = models.ForeignKey('payment.Account', on_delete=models.CASCADE, blank=True, null=True, related_name="received_to_account", default=None)
    document_no = models.CharField(max_length=64, verbose_name=_("Reference No"), blank=True, null=True)
    class Meta:
        # set_indian_status permission
        permissions = [
            ('print_agent_account_statement', 'Can Print Agent Account Statement'),
            ('print_agent_receipt_voucher', 'Can Print Agent Receipt Voucher'),
        ]
    def save(self):
        super().save()
        
        if self.received_to_account != None:
            try:
                try:
                    t = AccountTransaction.objects.get(agent_payment_transaction=self)
                    t.company = self.company
                    t.account = self.received_to_account
                    if self.transaction_type == 'c':
                        t.credit = self.amount
                        t.debit = 0.00
                    else:
                        t.credit = 0.00
                        t.debit = self.amount
                    
                    t.discription = self.payment_for
                    t.date = self.date
                    t.time = self.time
                    t.performed_by = self.performed_by
                    t.document_no = self.document_no
                    t.save()
                    
                except:
                    t = AccountTransaction.objects.get(agent_payment_transaction=self)
                    t.company = self.company
                    t.account = self.received_to_account
                    if self.transaction_type == 'c':
                        t.credit = self.amount
                        t.debit = 0.00
                    else:
                        t.credit = 0.00
                        t.debit = self.amount
                    t.discription = self.payment_for
                    t.date = self.date
                    t.time = self.time
                    t.performed_by = self.performed_by
                    
                    t.document_no = self.document_no
                    t.save()
            except ObjectDoesNotExist:
                t = AccountTransaction()
                t.company = self.company
                t.account = self.received_to_account
                t.credit = self.amount
                t.debit = 0.00
                t.discription = self.payment_for
                t.date = self.date
                t.time = self.time
                t.performed_by = self.performed_by
                t.agent_payment_transaction = self
                t.document_no = self.document_no
                t.save()
        super().save()
        
    def delete(self):
        try:
            t = AccountTransaction.objects.get(agent_payment_transaction=self)
            t.delete()
        except:
            pass
        super().delete()
    
    def transaction_balance(self):
        if self.transaction_type == 'c':
            return self.amount
        elif self.transaction_type == 'd':
            return self.amount * -1

        
        


class OfficeExpense(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Amount"))
    payment_by = models.CharField(max_length=16, verbose_name=_("Payment method"), choices=payment_by)
    date= models.DateField(_("Date"))
    bill_no = models.CharField(_("Bill No"), max_length=50, null = True, blank=True)
    reason = models.CharField(max_length=64, verbose_name=_("Reason"))
    paid_to = models.CharField(_("Paid to"), max_length=50)
    accountant = models.CharField(_("Accountant"), max_length=50)
    transaction = models.ForeignKey('payment.CompanyTreasuryTransaction', on_delete=models.CASCADE, unique=True, blank=True, null=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )


    def save(self, *args, **kwargs):
        try:
            t = CompanyTreasuryTransaction.objects.get(id=self.transaction, transaction_type='d')
            t.amount = self.amount
            t.save()
            self.transaction = t
            
        except ObjectDoesNotExist:
            t = CompanyTreasuryTransaction()
            t.company = self.company
            t.amount = self.amount
            t.transaction_type = 'd'
            t.transaction_for = 'company_expense'
            t.reason = self.reason
            t.date = self.date
            t.performed_by = self.accountant
            t.received_by = self.paid_to

            t.save()
            self.transaction = t
        
        super().save(*args, **kwargs)




    
    def delete(self, *args, **kwargs):
        try:
            t = CompanyTreasuryTransaction.objects.get(id=self.transaction.id)
            t.delete()
        except:
            pass
        super().delete(*args, **kwargs)



class CompanyTreasuryTransaction(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Amount"))
    transaction_type = models.CharField(max_length=16, verbose_name="Transaction Type", choices=wallet_transaction_type)
    transaction_for = models.CharField(max_length=16, verbose_name="Payment for", choices=treasury_payment_types, default='general')

    reason = models.CharField(max_length=64, verbose_name=_("Reason"))
    payment_by = models.CharField(max_length=16, verbose_name=_("Paid by"), choices=payment_by)
    date= models.DateField(_("Date"))
    time= models.TimeField(_("Time"), auto_now=True, null=True)
    performed_by = models.CharField(max_length=64, verbose_name=_("Collected from"))
    # voucher = models.ForeignKey('voucher.AgentVoucher', on_delete=models.CASCADE, blank=True, null=True)
    received_by = models.CharField(max_length=64, verbose_name=_("Received By"), blank=True, null=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )

class Payroll(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))
    history = HistoricalRecords(
        user_model='auth.User',
    )
    
    
    def amount(self):
        amount = 0.00
        employees = EmployeeSalary.objects.filter(payroll = self)
        for e in employees:
            amount += float(e.net_salary())
        return amount
    
    def employee_count(self):
        employees = EmployeeSalary.objects.filter(payroll = self).count()
        
        return employees
    

    def status(self):
        approved_count = EmployeeSalary.objects.filter(payroll = self, status = "")






        
class EmployeeSalary(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    employee = models.ForeignKey('company.Employee', on_delete=models.PROTECT)
    payroll = models.ForeignKey('payment.Payroll', on_delete=models.PROTECT, null=True, blank=True)
    salary = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Monthly Salary"), default=0.00)
    absent_days = models.IntegerField(verbose_name=_('Absent Days'), default=0)
    status = models.CharField(verbose_name=_('Status'), max_length=64, choices=salary_collection_status, default="pending")
    collected_amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Collected Amount"), default=0.00)
    history = HistoricalRecords(
        user_model='auth.User',
    )

    # def per_day_wage(self):
    #     monthly_salary = self.employee.salary
    #     per_day_wage = round(monthly_salary / 30, 2)
    #     return round(float(per_day_wage, 2))

    def net_salary(self):
        salary = self.employee.salary
        # absent_amount = float(self.per_day_wage) * float(self.absent_days)
        # amount = round(salary - absent_amount, 2)
        return salary
    

    
class SupplierPaymentTransaction(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Amount"))
    transaction_type = models.CharField(max_length=16, verbose_name="Transaction Type", choices=wallet_transaction_type)
    transaction_for = models.CharField(max_length=16, verbose_name="Payment for", choices=treasury_payment_types, default='general')
    payment_by = models.CharField(max_length=16, verbose_name=_("Paid by"), choices=payment_by)
    date= models.DateField(_("Date"))
    time= models.TimeField(_("Time"), auto_now=True, null=True)
    voucher = models.ForeignKey('voucher.AgentVoucher', on_delete=models.CASCADE, blank=True, null=True)
    payment_by = models.CharField(max_length=64, verbose_name=_("Payment from"))
    received_by = models.CharField(max_length=64, verbose_name=_("Received By"), blank=True, null=True)

    is_settlement_transaction = models.BooleanField(default=False)
    history = HistoricalRecords(
        user_model='auth.User',
    )


# class Account(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
#     account_name_en = models.CharField(max_length=64, verbose_name=_("Account Name English"))
#     account_name_ar = models.CharField(max_length=64, verbose_name=_("Account Name Arabic"))

#     def __str__(self):
#         if get_language() == "ar":
#             return self.account_name_ar
#         return self.account_name_en

#     class Meta:
#         unique_together = ['company', 'account_name_en']
#         verbose_name = _("Account")
#         verbose_name_plural = _("Accounts")

#         permissions = [
#             ('print_account_statement', 'Can Print Account Statement'),
#             ('print_account_receipt_voucher', 'Can Print Account Receipt Voucher'),
            
#         ]


#     def balance(self):
#         balance = 0.00
#         credit = 0.00
#         debit = 0.00
#         transactions = AccountTransaction.objects.filter(account=self)
#         for t in transactions:
#             credit += float(t.credit)
#             debit += float(t.debit)
#         balance = credit - debit
#         return balance
    

# class AccountTransaction(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
#     account = models.ForeignKey(Account, on_delete=models.PROTECT)
#     debit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Debit"), default=0.00)
#     credit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Credit"), default=0.00)
#     discription = models.CharField(max_length=64, verbose_name=_("Discription"))
#     date= models.DateField(_("Date"))
#     time= models.TimeField(_("Time"), auto_now=True, null=True)
#     performed_by = models.CharField(max_length=64, verbose_name=_("Performed By"))
#     received_by = models.CharField(max_length=64, verbose_name=_("Received By"), blank=True, null=True)
#     transfer_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_to", blank=True, null=True)
#     transfer_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfer_from", blank=True, null=True)
#     parent_transaction = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
#     paid_to = models.CharField(max_length=64, verbose_name=_("Paid To"), blank=True, null=True)
#     received_from = models.CharField(max_length=64, verbose_name=_("Received From"), blank=True, null=True)

#     document_no = models.CharField(max_length=64, verbose_name=_("Reference No"), blank=True, null=True)

#     # This field is to store AgentPaymentTransaction if agent payment is selected
#     agent_payment_transaction = models.ForeignKey('payment.AgentPaymentTransaction', on_delete=models.CASCADE, blank=True, null=True, related_name="agent_payment_transaction")
    
#     is_settlement_transaction = models.BooleanField(default=False)
#     history = HistoricalRecords(
#         user_model='auth.User',
#     )

    

    
#     def __str__(self):
#         return self.discription
    
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.debit > 0:
#             if self.transfer_to != None:
#                 if self.parent_transaction == None:
#                     try:
#                         transfer = AccountTransaction()
#                         transfer.company = self.company
#                         transfer.account = self.transfer_to
#                         transfer.credit = self.debit
#                         transfer.discription = self.discription
#                         transfer.date = self.date
#                         transfer.time = self.time
#                         transfer.performed_by = self.performed_by
#                         transfer.parent_transaction = self
#                         transfer.transfer_from = self.account
#                         transfer.document_no = self.document_no
#                         transfer.save()
#                     except:
#                         print("Error")
#                         pass
#                 else:
#                     try:
#                         transfer = AccountTransaction.objects.get(parent_transaction=self)
#                         transfer.company = self.company
#                         transfer.account = self.transfer_to
#                         transfer.credit = self.debit
#                         transfer.discription = self.discription
#                         transfer.date = self.date
#                         transfer.time = self.time
#                         transfer.performed_by = self.performed_by
#                         transfer.transfer_from = self.account
#                         transfer.document_no = self.document_no
#                         transfer.save()
#                     except:
#                         print("Error")
#                         pass
#         super().save(*args, **kwargs)


# # class SupplierAccount(models.Model):
# #     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
# #     supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT)

# #     def __str__(self):
# #         return self.supplier
    


# # class SupplierAccountTransaction(models.Model):
# #     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
# #     supplier = models.ForeignKey(SupplierAccount, on_delete=models.PROTECT)
# #     debit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Debit"), default=0.00)
# #     credit = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Credit"), default=0.00)
# #     discription = models.CharField(max_length=64, verbose_name=_("Discription"))
# #     date= models.DateField(_("Date"))
# #     time= models.TimeField(_("Time"), auto_now=True, null=True)
# #     performed_by = models.CharField(max_length=64, verbose_name=_("Performed By"))
# #     received_by = models.CharField(max_length=64, verbose_name=_("Received By"), blank=True, null=True)
# #     paid_to = models.CharField(max_length=64, verbose_name=_("Paid To"), blank=True, null=True)
# #     received_from = models.CharField(max_length=64, verbose_name=_("Received From"), blank=True, null=True)

# #     transport_invoice = models.ForeignKey('voucher.TransportInvoice', on_delete=models.CASCADE, blank=True, null=True)


    

    
# #     def __str__(self):
# #         return self.discription
    
# #     def save(self, *args, **kwargs):
# #         super().save(*args, **kwargs)
# #         if self.debit > 0:
# #             if self.transfer_to != None:
# #                 if self.parent_transaction == None:
# #                     try:
# #                         transfer = SupplierAccountTransaction()
# #                         transfer.company = self.company
# #                         transfer.supplier = self.supplier
# #                         transfer.credit = self.debit
# #                         transfer.discription = self.discription
# #                         transfer.date = self.date
# #                         transfer.time = self.time
# #                         transfer.performed_by = self.performed_by
# #                         transfer.parent_transaction = self
# #                         transfer.transfer_from = self.account
                        
# #                         transfer.save()
# #                     except:
# #                         print("Error")
# #                         pass
# #                 else:
# #                     try:
# #                         transfer