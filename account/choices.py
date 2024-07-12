
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

account_level_choices = (
    (1, _('Level 1')),
    (2, _('Level 2')),
    (3, _('Level 3')),
    (4, _('Level 4')),
    (5, _('Level 5')),
)