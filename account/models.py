from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.db.models import Avg, Count, Min, Sum
from .choices import payment_method_choices, payment_method_choices_settlement, account_level_choices
from simple_history.models import HistoricalRecords
from decimal import Decimal
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import transaction as db_transaction
from account.manager import TransactionManager
from num2words import num2words
from datetime import datetime
import pytz
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.




def delete_allowed(company, obj):
    # object last edit timestamp
    last_edit = obj.history.last().history_date
    allowd_hours = company.settings().delete_hours

    # current time in UTC
    current_time = datetime.now(pytz.utc)

    # calculate the difference between the last edit and the current time
    diff = current_time - last_edit

    # if the difference is less than the allowed hours return True
    if diff.total_seconds() / 3600 < allowd_hours:
        return True
    return False

def edit_allowed(company, obj):
    # object last edit timestamp
    last_edit = obj.history.last().history_date
    allowd_hours = company.settings().edit_hours

    # current time in UTC
    current_time = datetime.now(pytz.utc)

    # calculate the difference between the last edit and the current time
    diff = current_time - last_edit

    # if the difference is less than the allowed hours return True
    if diff.total_seconds() / 3600 < allowd_hours:
        return True
    return False
    


class FinancialYear(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Financial Year")
        verbose_name_plural = _("Financial Years")
    
    def __str__(self):
        return f"{self.start_date} - {self.end_date}"
    
    def save(self, *args, **kwargs):
        # check if there is an active financial year
        active_financial_year = FinancialYear.objects.filter(company=self.company, is_active=True).first()
        if active_financial_year:
            # if there is an active financial year, deactivate it
            active_financial_year.is_active = False
            active_financial_year.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # check if there is an active financial year
        active_financial_year = FinancialYear.objects.filter(company=self.company, is_active=True).first()
        if active_financial_year:
            # if there is an active financial year, deactivate it
            active_financial_year.is_active = False
            active_financial_year.save()
        
        super().delete(*args, **kwargs)



class Account(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    account_name_en = models.CharField(max_length=64, verbose_name=_("Account Name English"))
    account_name_ar = models.CharField(max_length=64, verbose_name=_("Account Name Arabic"))
    account_type = models.CharField(max_length=1, choices=(
        ('A', _("Asset")),
        ('L', _("Liability")),
        ('E', _("Equity")),
        ('R', _("Revenue")),
        ('X', _("Expense")),
    ), verbose_name=_("Account Type"))
     # This is the account number that will be used in the chart of accountsو it will be generated automatically
    account_number = models.CharField(max_length=64, verbose_name=_("Account Number"), null=True, blank=True, editable=False)
    
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True, related_name='child_accounts', )
    # allow_child_accounts = models.BooleanField(default=False, verbose_name=_("Allow Child Accounts"))
    level = models.IntegerField(choices=account_level_choices, verbose_name=_("Account Level"), default=1)

    allow_edit = models.BooleanField(default=True, verbose_name=_("Allow Edit"))


    class Meta:
        verbose_name = _("Company Account")
        verbose_name_plural = _("Company Accounts")
        permissions = [
            ('can_view_agent_account', 'Can View Agent Account'),
            ('can_view_transport_company_account', 'Can View Transport Company Account'),
            ('can_view_internal_account', 'Can View Internal Account'),
            ('can_view_accounts_tree', 'Can View Accounts Tree'),

        ]

    def save(self, *args, **kwargs):
        # Generate account number
        if not self.account_number:
            if self.parent_account:
                child_accounts = Account.objects.filter(parent_account=self.parent_account)
                self.account_number = f"{self.parent_account.account_number}{str(child_accounts.count()+1).zfill(3)}"
                self.account_type = self.parent_account.account_type
            else:
                self.account_number = str(Account.objects.filter(company=self.company).count()+1)
        
        self.level = self.set_account_level()
        

        super(Account, self).save(*args, **kwargs)

        # Update child accounts
        if self.parent_account:
            child_accounts = Account.objects.filter(parent_account=self)
            for i, child_account in enumerate(child_accounts):
                child_account.account_number = f"{self.account_number}{str(i+1).zfill(3)}"
                child_account.save()


    
        

    class Meta:
        unique_together = ['company', 'account_name_en']
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

        permissions = [
            ('print_account_statement', 'Can Print Account Statement'),
            ('print_account_receipt_voucher', 'Can Print Account Receipt Voucher'),
            ('can_view_agent_account', 'Can View Agent Account'),
            ('can_view_transport_company_account', 'Can View Transport Company Account'),
            ('can_view_internal_account', 'Can View Internal Account'),
            ('can_view_accounts_tree', 'Can View Accounts Tree'),
            
            
        ]

    def __str__(self):
        parent_account = self.parent_account_name()
        if parent_account:
            if get_language() == 'ar':
                return f"{self.account_number} - ({parent_account}) {self.account_name_ar}"
            return f"{self.account_number} - ({parent_account}) {self.account_name_en}"
        else:
            if get_language() == 'ar':
                return f"{self.account_number} - {self.account_name_ar}"
            return f"{self.account_number} - {self.account_name_en}"
        
    def allow_child_accounts(self):
        if self.level == 5:
            return False
        return True
        
    def name(self):
        if get_language() == 'ar':
            return self.account_name_ar
        return self.account_name_en


    def child_accounts(self):
        return Account.objects.filter(parent_account=self)


    def parent_account_name(self):
        if self.parent_account:
            return self.parent_account.name()
        return None

    def balance_debit(self):
        return self.journalentry_set.aggregate(models.Sum('debit'))['debit__sum'] or Decimal('0.00')

    def balance_credit(self):
        return self.journalentry_set.aggregate(models.Sum('credit'))['credit__sum'] or Decimal('0.00')
    def code(self):
        return self.account_number
    
    def account_level(self):
        # calculate account level in the chart of accounts
        if self.parent_account:
            return self.parent_account.account_level() + 1
        return 1
    
    def parent(self):
        return self.parent_account or None
    
    # calculate balance of child accounts which is the sum of all child accounts balance
    def child_accounts_credit(self):
        return self.child_accounts.aggregate(Sum('balance_credit'))['balance_credit__sum'] or Decimal('0.00')
    
    def child_accounts_debit(self):
        return self.child_accounts.aggregate(Sum('balance_debit'))['balance_debit__sum'] or Decimal('0.00')
    
    # calculate account balance like assets, liabilities, equity, revenue, and expense
    def balance(self):

        balance = 0.00

        if self.account_type in ['A', 'E', 'R']:
            balance = self.balance_debit() - self.balance_credit()
            return round(balance,2)
        elif self.account_type in ['L', 'X']:
            balance = self.balance_credit() - self.balance_debit()
            return round(balance,2)
        
    def balance_color(self):
        try:
            if self.balance() >= 0.00 and self.account_type in ['A', 'E', 'R']:
                return 'text-danger'
            elif self.balance() < 0.00 and self.account_type in ['A', 'E', 'R']:
                return 'text-success'
            elif self.balance() >= 0.00 and self.account_type in ['L', 'X']:
                return 'text-success'
            elif self.balance() < 0.00 and self.account_type in ['L', 'X']:
                return 'text-danger'
        except:
            return 'text-dark'
    def set_account_level(self):
        if self.parent_account:
            if self.parent_account.account_level() == 5:
                return ValidationError(_("You can't add more child accounts to this account"))
            return self.parent_account.account_level() + 1
        return 1
        
        
        
        



class Transaction(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    financial_year = models.ForeignKey('account.FinancialYear', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(verbose_name=_("Date"))
    description_en = models.CharField(max_length=256, verbose_name=_("Description English"), null=True, blank=True)
    description_ar = models.CharField(max_length=256, verbose_name=_("Description Arabic"), null=True, blank=True)
    reference_no = models.CharField(max_length=256, verbose_name=_("Reference"), null=True, blank=True)


    history = HistoricalRecords(
        user_model='auth.User',
    )

    objects = TransactionManager()


    def delete(self, *args, **kwargs):
        check = delete_allowed(self.company, self)
        if check:
            super().delete(*args, **kwargs)

        else:
            raise ValidationError(_("You are not allowed to delete this transaction"))
    



    def description(self):
        if get_language() == 'ar':
            return self.description_ar
        return self.description_en
    


    def username(self):
        if self.history.exists():
            return self.history.last().history_user
        else:
            return _('Unknown')
        

    def debit(self):
        debit = round(Decimal(self.entries.aggregate(models.Sum('debit'))['debit__sum']),2) or Decimal('0.00')
        return debit
    
    def credit(self):
        credit =  round(Decimal(self.entries.aggregate(models.Sum('credit'))['credit__sum']),2) or Decimal('0.00')
        return credit
    
    def count_entries(self):
        return self.entries.count()
    

    def error_display(self):
        if self.debit() != self.credit():
            return _("Debit and Credit are not equal")
        return None
    
    def save(self, *args, **kwargs):
        self.financial_year = FinancialYear.objects.filter(company=self.company, is_active=True).first()
        super().save(*args, **kwargs)



class JournalEntry(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_("Date"))
    transaction = models.ForeignKey('account.Transaction', on_delete=models.CASCADE, blank=True, null=True, related_name='entries')
    description_en = models.CharField(max_length=256, verbose_name=_("Description English"), null=True, blank=True)
    description_ar = models.CharField(max_length=256, verbose_name=_("Description Arabic"), null=True, blank=True)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name=_("Account"), limit_choices_to={'level': 5})
    debit = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Debit"),default=0.00)
    credit = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Credit"),default=0.00)

    # this is to specify for what purpose this entry is made, like for example if it is made for a specific invoice or a specific payment
    entry_for = models.CharField(max_length=16, verbose_name=_("Entry For"), null=True)

    history = HistoricalRecords(
        user_model='auth.User',
    )

    def clean(self):
        if self.debit < 0.00 or self.credit < 0.00:
            raise ValidationError(_("Debit and Credit should be positive numbers"))
        
        # check if the account is of level 5 else raise an error
        if self.account.account_level() != 5:
            raise ValidationError(_("You can only select accounts of level 5"))
        if self.debit == 0.00 and self.credit == 0.00:
            raise ValidationError(_("Debit or Credit should be greater than 0.00"))
        if abs(self.debit > 0.00) and abs(self.credit > 0.00):
            raise ValidationError(_("You can only select either Debit or Credit"))
        

    def save(self, *args, **kwargs):
        self.date = self.transaction.date
        self.clean()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")
    
    def __str__(self):
        return f"{self.account} - {self.debit} - {self.credit}"
    
    def entry_amount(self):
        if self.account.account_type in ['A', 'E', 'R']:
            return self.debit - self.credit
        elif self.account.account_type in ['L', 'X']:
            return self.credit - self.debit
    
    def account_balance(self):
        # calculate account balance on this transaction formula will be balance = previous balance + debit - credit
        debit_before_entry = JournalEntry.objects.filter(company=self.company, account=self.account, date__lt=self.date).order_by('date', 'pk').aggregate(models.Sum('debit'))['debit__sum'] or 0
        credit_before_entry = JournalEntry.objects.filter(company=self.company, account=self.account, date__lt=self.date).order_by('date', 'pk').aggregate(models.Sum('credit'))['credit__sum'] or 0
        balance = debit_before_entry - credit_before_entry + self.debit - self.credit
        return balance
    
    def username(self):
        if self.history.exists():
            return self.history.last().history_user
        else:
            return _('Unknown')
    


        




class ReceiptVoucher(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_("Date"), blank=True, null=True)
    transaction = models.ForeignKey('account.Transaction', on_delete=models.CASCADE, blank=True, null=True)
    collected_from = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='collected_from_account',limit_choices_to={'level': 5})
    collected_from_name = models.CharField(max_length=64, verbose_name=_("Collected From"), null=True, blank=True, )
    to_account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='collected_to_account',limit_choices_to={'level': 5})
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(max_length=256, verbose_name=_("Description"))
    reference_no = models.CharField(max_length=64, verbose_name=_("Reference Number"), null=True, blank=True)
    payment_method = models.CharField(max_length=16, choices=payment_method_choices, verbose_name=_("Payment Method"), null=True, blank=True)

    history = HistoricalRecords(
        user_model='auth.User',
    )


    class Meta:
        verbose_name = _("Receipt Voucher")
        verbose_name_plural = _("Receipt Vouchers")
    
    def __str__(self):
        return f"{self.to_account} - {self.collected_from} - {self.amount}"
    def clean(self):
        if self.amount < 0.00:
            raise ValidationError(_("Amount should be a positive number"))
    
    def save(self, *args, **kwargs):
        self.clean()
        self.date = datetime.now()
        super().save(*args, **kwargs)
        
        credit_account = None
        debit_account = None
        
        
        

        if not self.transaction:
            transaction = Transaction.objects.create_transaction_with_entries(
            company=self.company,
            description_en= f"Receipt Voucher - {self.description}",
            description_ar= f"سند قبض - {self.description}",
            reference_no=self.reference_no,
            ledger_entries=[
                {
                'account': self.collected_from.id,
                'transaction_type': 'credit',
                'amount': self.amount,
                'entry_for': 'receipt_voucher_collected_from'
                },
                {
                'account': self.to_account.id,
                'transaction_type': 'debit',
                'amount': self.amount,
                'entry_for': 'receipt_voucher_to_account'
                }
            ]
            )

            self.transaction = transaction
            super().save(*args, **kwargs)
        else:
            # check edit allowed
            check = edit_allowed(self.company, self)
            if check:
                transaction = Transaction.objects.get(pk=self.transaction.pk)
                transaction.company = self.company
                transaction.date = self.date
                transaction.description_en = f"Receipt Voucher - {self.description}"

                transaction.description_ar = f"سند قبض - {self.description}"
                transaction.reference_no = self.reference_no
                transaction.save()

                # amount changed
                if transaction.entries.first().debit != self.amount or transaction.entries.last().credit != self.amount or transaction.entries.first().account != credit_account or transaction.entries.last().account != debit_account:
                    if self.collected_from.account_type in ['A', 'E', 'R']:
                        credit_account = self.collected_from
                        debit_account = self.to_account
                    elif self.collected_from.account_type in ['L', 'X']:
                        credit_account = self.to_account
                        debit_account = self.collected_from

                    # edit journal entries
                    debit_entry = transaction.entries.get(credit=0.00)
                    debit_entry.account = debit_account
                    debit_entry.debit = self.amount
                    debit_entry.save()

                    credit_entry = transaction.entries.get(debit=0.00)
                    credit_entry.account = credit_account
                    credit_entry.credit = self.amount
                    credit_entry.save()


            else:
                raise ValidationError(_("You are not allowed to edit this transaction"))
                

    def in_words(self):
        currency = self.company.settings().get_default_currency_display
        
        return num2words(self.amount, lang='ar', to="currency", )
        
    
    def delete(self, *args, **kwargs):
        check = delete_allowed(self.company, self)
        if check:
            transaction = Transaction.objects.get(pk=self.transaction.pk)
            transaction.delete()
            super().delete(*args, **kwargs)

        else:
            raise ValidationError(_("You are not allowed to delete this transaction"))


        


    
class PaymentVoucher(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_("Date"), blank=True, null=True)
    transaction = models.ForeignKey('account.Transaction', on_delete=models.CASCADE, blank=True, null=True)
    paid_to = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='paid_to_account', limit_choices_to={'level': 5})
    paid_to_name = models.CharField(max_length=64, verbose_name=_("Paid To"), null=True, blank=True)
    from_account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='paid_from_account', limit_choices_to={'level': 5})
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(max_length=256, verbose_name=_("Description"))
    reference_no = models.CharField(max_length=64, verbose_name=_("Reference Number"), null=True, blank=True)
    payment_method = models.CharField(max_length=16, choices=payment_method_choices, verbose_name=_("Payment Method"), null=True, blank=True)

    history = HistoricalRecords(
        user_model='auth.User',
    )

    class Meta:
        verbose_name = _("Payment Voucher")
        verbose_name_plural = _("Payment Vouchers")
    
    def __str__(self):
        return f"{self.from_account} - {self.paid_to} - {self.amount}"
    
    def clean(self):
        if self.amount < 0.00:
            raise ValidationError(_("Amount should be a positive number"))
    
    def save(self, *args, **kwargs):
        self.date = datetime.now()
        super().save(*args, **kwargs)
        

        
        

        if not self.transaction:
            transaction = Transaction.objects.create_transaction_with_entries(
            company=self.company,
            description_en=self.description,
            description_ar=self.description,
            reference_no=self.reference_no,
            ledger_entries=[
                {
                'account': self.paid_to.id,
                'transaction_type': 'debit',
                'amount': self.amount,
                'entry_for': 'payment_voucher_paid_to'
                },
                {
                'account': self.from_account.id,
                'transaction_type': 'credit',
                'amount': self.amount,
                'entry_for': 'payment_voucher_from_account'
                }
            ]
            )

            self.transaction = transaction
        
        else:
            # check edit allowed
            check = edit_allowed(self.company, self)
            if check:
                transaction = Transaction.objects.get(pk=self.transaction.pk)
                transaction.company = self.company
                transaction.date = self.date
                transaction.description_en = self.description
                transaction.description_ar = self.description
                transaction.reference_no = self.reference_no
                transaction.save()

                # amount changed
                if transaction.entries.first().debit != self.amount or transaction.entries.last().credit != self.amount or transaction.entries.first().account != credit_account or transaction.entries.last().account != debit_account:
                    if self.paid_to.account_type in ['A', 'E', 'R']:
                        credit_account = self.paid_to
                        debit_account = self.from_account
                    elif self.paid_to.account_type in ['L', 'X']:
                        credit_account = self.from_account
                        debit_account = self.paid_to

                    # edit journal entries
                    debit_entry = transaction.entries.get(credit=0.00)
                    debit_entry.account = debit_account
                    debit_entry.debit = self.amount
                    debit_entry.save()

                    credit_entry = transaction.entries.get(debit=0.00)
                    credit_entry.account = credit_account
                    credit_entry.credit = self.amount
                    credit_entry.save()

            else:
                raise ValidationError(_("You are not allowed to edit this transaction"))

        super().save(*args, **kwargs)

    def in_words(self):
        currency = self.company.settings().get_default_currency_display
        
        return num2words(self.amount, lang='ar', to="currency", )
    
    def delete(self, *args, **kwargs):
        check = delete_allowed(self.company, self)
        if check:
            transaction = Transaction.objects.get(pk=self.transaction.pk)
            transaction.delete()
            super().delete(*args, **kwargs)

        else:
            raise ValidationError(_("You are not allowed to delete this transaction"))
    


        


