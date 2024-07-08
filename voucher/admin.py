from django.contrib import admin
from .models import AgentVoucher, FixedVoucherPrices, TransportInvoice
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

admin.site.register(AgentVoucher, SimpleHistoryAdmin)
admin.site.register(FixedVoucherPrices, SimpleHistoryAdmin)
admin.site.register(TransportInvoice, SimpleHistoryAdmin)

