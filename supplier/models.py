from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

# Create your models here.
class Supplier(models.Model):
    company = models.ForeignKey('company.Company', verbose_name=_('Company'), on_delete=models.CASCADE)
    name_en = models.CharField(_('Name'), max_length=255)
    name_ar = models.CharField(_('Name'), max_length=255)
    cr_no = models.CharField(_('CR No'), max_length=255)
    vat_no = models.CharField(_('VAT No'), max_length=255)
    vat_percentage = models.FloatField(_('VAT Percentage'), default=15)
    email = models.EmailField(_('Email'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=255)
    address = models.CharField(_('Address'), max_length=255)
    is_transport_company = models.BooleanField(_('Is Transport Company'), default=False)
    history = HistoricalRecords(
        user_model='auth.User',
    )

    
    def __str__(self):
        if get_language() == "ar":
            return self.name_ar
        return self.name_en
    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ('name_en', 'name_ar', 'company')
        unique_together = ('name_en', 'name_ar', 'company')