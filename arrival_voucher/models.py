from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import *
from transport.models import TransportPurchaseInvoice

from simple_history.models import HistoricalRecords
# from transport.models import TransportCompany
# Create your models here.

status_choices = (
    ('pending', _('Pending')),
    ('sent', _('Sent to Transport')),
    ('approved', _('Approved')),
    ('confirmed', _('Confirmed')),
    ('rejected', _('Rejected')),
    ('draft', _('Draft')),
    ('with_agent_draft', _('Draft, with agent')),
    ('with_agent_rejected', _('Rejected, sent back to agent')),
)


voucher_accounts_status_choices = (
    ('pending', _('Pending')),
    ('sent', _('Sent to Accounts')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected'))
)



transport_status_choices = (
    ('pending', _('Pending')),
    ('sent', _('Sent to Transport')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
    ('draft', _('Draft')),
)

rawdah_status_choices = (
    ('pending', _('Pending')),
    ('reserved', _('Reserved')),
    ('completed', _('Completed')),
    ('not_available', _('Not Available')),
)


accounts_status_choices = (
    ('draft', _('Draft')),
    ('pending', _('Pending')),
    ('approved', _('Approved')),
    ('query', _('Query')),
    ('updated_pending', _('Updated, Pending Approval')),
)


# class TransportInvoice(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
#     agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT   , verbose_name=_("Agent"))
#     date = models.DateField(verbose_name=_("Date"),default=datetime.date.today)
#     # voucher = models.ForeignKey('Voucher', on_delete=models.PROTECT, null=True, blank=True)
#     purchase_invoice = models.ForeignKey('PurchaseInvoice', on_delete=models.PROTECT, null=True, blank=True)
#     supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT, null=True, blank=True)
#     transport_type = models.CharField(max_length=255,verbose_name=_("Transport type"), choices=TRANSPORT_TYPE)
#     qty = models.IntegerField(verbose_name=_("Quantity"), db_column='qty', default=1)
#     price = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Price"))
#     tax_percentage = models.DecimalField(max_digits=65, decimal_places=2,verbose_name=_("Tax Percentage"), null=True, blank=True)
#     description = models.CharField(max_length=255,verbose_name=_("Description"), null=True, blank=True)
#     arrival_voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.PROTECT, null=True, blank=True)
#     referance_no = models.CharField(max_length=255,verbose_name=_("Reference No"), null=True, blank=True)
#     additional_movement = models.BooleanField(verbose_name=_("Additional Movement"), default=False, blank=True, null=True, )
#     movement = models.ForeignKey('transport.TransportMovement', on_delete=models.SET_NULL, blank=True, null=True, related_name='movement', verbose_name=_("Movement"))
    
    


class ArrivalVoucher(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT)
    country = models.ForeignKey('core.Country', on_delete=models.PROTECT, verbose_name=_('Country'),null=True, blank=False)
    agent_referance_no = models.CharField(verbose_name=_('Agent Reference No'), max_length=256, null=True, blank=True)
    group_name = models.CharField(verbose_name=_('Group name'), max_length=32,null=True, blank=True)
    group_no = models.CharField(verbose_name=_('Group no'), max_length=256)
    pax = models.IntegerField(verbose_name=_('PAX'))
    group_leader = models.CharField(verbose_name=_('Group leader name'),max_length=32,null=True, blank=True)
    group_leader_contact = models.CharField(verbose_name=_('Group leader contact'),null=True, blank=True, max_length = 32)
    transport_company = models.ForeignKey('transport.TransportCompany',verbose_name=_('Transport company'),null=True, blank=True, on_delete=models.PROTECT)
    transport_brn = models.CharField(verbose_name=_('Transport BRN'), max_length=256, null=True, blank=True)
    transportation_type = models.CharField(verbose_name=_('Transportation Type'), max_length=32,null=True, blank=True, choices=transportation_type)
    transport_type = models.ForeignKey('transport.TransportType',verbose_name=_('Transport Type'),null=True, blank=True, on_delete=models.PROTECT)
    # Arrival Flight Information
    arrival_flight_no = models.CharField(verbose_name=_('Arrival Flight No'), max_length=32,null=True, blank=True)
    arrival_airport = models.CharField(verbose_name=_('Arrival Airport'), max_length=32,null=True, blank=True, choices=saudi_airports)
    arrival_date = models.DateField(_("Arrival Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    arrival_time = models.TimeField(_("Arrival Time"), auto_now=False, auto_now_add=False, null=True, blank=True)

    # Departure Flight Information
    departure_flight_no = models.CharField(verbose_name=_('Departure Flight No'), max_length=32,null=True, blank=True)
    departure_airport = models.CharField(verbose_name=_('Departure Airport'), max_length=32,null=True, blank=True, choices=saudi_airports)
    departure_date = models.DateField(_("Departure Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    departure_time = models.TimeField(_("Departure Time"), auto_now=False, auto_now_add=False, null=True, blank=True)

    # Makkah Hotel
    makkah_hotel = models.CharField(verbose_name=_('Makkah Hotel'), max_length=64, null=True, blank=True)

    # Medina Hotel
    medina_hotel = models.CharField(verbose_name=_('Medina Hotel'), max_length=64, null=True, blank=True)

    # status
    status = models.CharField(verbose_name=_('Status'), max_length=32, choices=status_choices, default='draft')
    rejected_reason = models.TextField(verbose_name=_('Rejected Reason'), null=True, blank=True)
    # history = HistoricalRecords(
    #     user_model='auth.User',
    # )

    # Rawdah Permits
    rawdah_men_request_date = models.DateField(_("Men Request Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    rawdah_women_request_date = models.DateField(_("Women Request Date"), auto_now=False, auto_now_add=False, null=True, blank=True)

    rawdah_men_reservation_date = models.DateField(_("Men Reservation Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    rawdah_men_reservation_time = models.TimeField(verbose_name=_("Men Reservation Time"), auto_now=False, auto_now_add=False, null=True, blank=True)
    rawdah_men_status = models.CharField(verbose_name=_("Men Status"), max_length=32, choices=rawdah_status_choices, default='pending')
    rawdah_women_reservation_date = models.DateField(_("Women Reservation Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    rawdah_women_reservation_time = models.TimeField(verbose_name=_("Women Reservation Time"), auto_now=False, auto_now_add=False, null=True, blank=True)
    rawdah_women_status = models.CharField(verbose_name=_("Women Status"), max_length=32, choices=rawdah_status_choices, default='pending')


    transport_status = models.CharField(verbose_name=_('Transport Status'), max_length=32, choices=transport_status_choices, default='draft')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    transport_package = models.ForeignKey('transport.TransportPackage', on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Transport Package"))
    purchase_invoice = models.ForeignKey('invoice.TransportPurchaseInvoice', on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Purchase Invoice"), editable=False)
    package_purchase_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Package Purchase Amount"), default=0.00)
    package_sale_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Package Sale Amount"), default=0.00)
    sale_invoice = models.ForeignKey('voucher.TransportInvoice', on_delete=models.PROTECT, blank=True, null=True, editable=False)
    


    accounts_status = models.CharField(verbose_name=_('Accounts Status'), max_length=32, choices=voucher_accounts_status_choices, default='pending')

    voucher_remarks = models.TextField(verbose_name=_('Voucher Remarks'), null=True, blank=True)

    transport_remarks = models.TextField(verbose_name=_('Transport Remarks'), null=True, blank=True)


    remarks_for_accounts = models.TextField(verbose_name=_('Remarks for Accounts'), null=True, blank=True)


    accounts_status = models.CharField(verbose_name=_('Accounts Status'), max_length=32, choices=accounts_status_choices, default='draft')


    


    def allow_agent_edit(self):
        if self.status == 'draft':
            return True
        elif self.status == 'pending':
            return False
        elif self.status == 'approved':
            return False
        elif self.status == 'rejected':
            return True

    def allow_submit(self):
        if self.status == 'draft':
            return True
        elif self.status == 'pending':
            return False
        elif self.status == 'approved':
            return False
        elif self.status == 'rejected':
            return True
        
    
    def total_movement(self):
        return self.transportmovement_set.count()
    
    def total_movements_completed(self):
        return self.transportmovement_set.filter(status='completed').count()
    
    def voucher_routes(self):
        # return routes of all movements linked to this voucher
        movements = self.transportmovement_set.all()
        routes = []
        for movement in movements:
            routes.append(movement.route)
        return routes
    
    def starting_date(self):
        movements = self.transportmovement_set.all().order_by('date', 'time')
        if movements:
            return movements[0].date
        return None
    
    class Meta:
        permissions = (("can_add_extra_movement", "Can add extra movement"),
                       ('can_delete_movement', 'Can delete movement'),
                       ('can_change_movement_date', 'Can change movement date'),
                       ('can_change_movement_status_after_completed', 'Can change movement status after completed'),
                        ('can_view_arrival_voucher_invoice', 'Can view arrival voucher invoice'),

                       )
    


    def __str__(self):
        return f"""
        {_("Transport Program")} UP-{self.pk} {_('total movements')} {self.total_movement()}

        """
     

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.package_purchase_amount > 0.00: 


            if self.purchase_invoice:
                invoice = TransportPurchaseInvoice.objects.get(pk=self.purchase_invoice.pk)
                invoice.company = self.company
                invoice.transport_company = self.transport_company
                print(self.transport_company)
                invoice.arrival_voucher = self
                invoice.date = self.date_created
                invoice.amount = self.package_purchase_amount
                invoice.save()
                self.purchase_invoice = invoice
                invoice.save()
            else:
                invoice = TransportPurchaseInvoice()
                invoice.company = self.company
                invoice.transport_company = self.transport_company
                invoice.arrival_voucher = self
                invoice.date = self.date_created
                invoice.amount = self.package_purchase_amount
                invoice.save()
                self.purchase_invoice = invoice
                super().save(*args, **kwargs)
                
        elif self.package_purchase_amount <= 0.00 :
            if self.purchase_invoice:
                invoice = TransportPurchaseInvoice.objects.get(pk=self.purchase_invoice.pk)
                self.purchase_invoice = None
                self.save()
                invoice.delete()
                super().save(*args, **kwargs)
            else:
                pass
        from voucher.models import TransportInvoice
        if self.package_sale_amount > 0.00:
            if self.sale_invoice:
                invoice = TransportInvoice.objects.get(pk=self.sale_invoice.pk)
                invoice.company = self.company
                invoice.agent = self.agent
                invoice.date = self.starting_date()
                invoice.voucher = self
                invoice.transport_type = self.transport_type or None
                invoice.qty = 1
                invoice.price = self.package_sale_amount
                invoice.description = str('Transport Invoice, Voucher no. UP-' + str(self.pk) + '-' + 'فاتورة النقل, رقم البرنامج UP-' + str(self.pk))
                invoice.referance_no = self.agent_referance_no
                invoice.save()
                self.sale_invoice = invoice
                invoice.save()

                
            else:
                invoice = TransportInvoice()
                invoice.company = self.company
                invoice.agent = self.agent
                invoice.date = self.starting_date()
                invoice.voucher = self
                invoice.transport_type = self.transport_type or None
                invoice.qty = 1
                invoice.price = self.package_sale_amount
                invoice.description = str('Transport Invoice, Voucher no. UP-' + str(self.pk) + '-' + 'فاتورة النقل, رقم البرنامج UP-' + str(self.pk))
                invoice.referance_no = self.agent_referance_no
                invoice.save()
                self.sale_invoice = invoice
            super().save(*args, **kwargs)
            
        elif self.package_sale_amount <= 0.00:
            if self.sale_invoice:
                invoice = TransportInvoice.objects.get(pk=self.sale_invoice.pk)
                self.sale_invoice = None
                self.save()
                invoice.delete()
                super().save(*args, **kwargs)
            else:
                pass
        else:
            pass

        for route in self.transportmovement_set.all():
            if route.outside_package == False:
                route.transport_company = self.transport_company
                
                route.type = self.transport_type
                route.save()
                super().save(*args, **kwargs)
            else:
                pass

    def delete(self, *args, **kwargs):
        if self.purchase_invoice:
            self.purchase_invoice.delete()
        if self.sale_invoice:
            self.sale_invoice.delete()

            
        
        super().save(*args, **kwargs)


class ArrivalVoucherGroups(models.Model):
    voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.CASCADE)
    agent = models.ForeignKey('agent.Agent', on_delete=models.CASCADE)
    # group = models.ForeignKey('visa_group.VisaGroup', on_delete=models.CASCADE)
    pax = models.IntegerField()


    



class ArrivalVoucherChat(models.Model):
    voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.user} {self.date_created}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.voucher.save()
        
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.voucher.save()


