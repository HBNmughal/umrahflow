from django.utils.translation import gettext_lazy as _


service_order_status = (
    (('draft'), _('Draft')),
    (('waiting'), _('Waiting for Approval')),
    (('approved'), _('Approved')),
    (('rejected'), _('Rejected')),
)


arrival_types = (
    (('air'), _('Air')),
    (('land'), _('Land')),
    (('sea'), _('Sea')),
)
