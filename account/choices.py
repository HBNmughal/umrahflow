
from django.utils.translation import gettext_lazy as _, get_language


payment_method_choices = (
    ('cash', _('Cash')),
    ('cheque', _('Cheque')),
    ('bank_transfer', _('Bank Transfer')),
    ('card', _('Credit Card / Debit Card')),
    ('other', _('Other')),
)


payment_method_choices_settlement = (
    ('settlement', _('Settlement')),
)