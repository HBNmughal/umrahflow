from django.contrib import admin
from .models import Account, Transaction, JournalEntry, ReceiptVoucher, AccountSettlementCredit, AccountSettlementDebit
from simple_history.admin import SimpleHistoryAdmin



# Register your models here.


admin.site.register(Account)
admin.site.register(Transaction,SimpleHistoryAdmin)
admin.site.register(JournalEntry)
admin.site.register(ReceiptVoucher)
admin.site.register(AccountSettlementCredit)
admin.site.register(AccountSettlementDebit)

