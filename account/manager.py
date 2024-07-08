from django.db import models
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class TransactionManager(models.Manager):

    def create_transaction_with_entries(self, company, description_en, description_ar, reference_no, ledger_entries):
        # Validate total debits and credits
        total_debits = Decimal(0.00)
        total_credits = Decimal(0.00)
        for entry in ledger_entries:
            if entry is None:
                continue
            if entry['transaction_type'] == 'debit':
                total_debits += entry['amount']
            else:
                total_credits += entry['amount']
        if total_debits != total_credits:
            raise ValidationError(_(f"Total debits and credits should be equal. Total debits: {total_debits}, Total credits: {total_credits}")) 
        
        if len(ledger_entries) < 2:
            raise ValidationError(_("Transaction should have at least 2 entries"))
        
        with db_transaction.atomic():


            # Create the transaction
            
            transaction = self.create(company=company, description_en=description_en, description_ar=description_ar, reference_no=reference_no)
            # Create the journal entries
            for entry in ledger_entries:
                from account.models import Account, JournalEntry

                if entry is None:
                    continue
                account = Account.objects.get(pk=entry['account'])
                if entry['transaction_type'] == 'debit':
                    JournalEntry.objects.create(company=company, transaction=transaction, account=account, debit=entry['amount'], credit=0.00, entry_for=entry['entry_for'] if 'entry_for' in entry else None)
                else:
                    JournalEntry.objects.create(company=company, transaction=transaction, account=account, debit=0.00, credit=entry['amount'], entry_for=entry['entry_for'] if 'entry_for' in entry else None)
            return transaction