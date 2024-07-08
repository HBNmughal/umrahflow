from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from simple_history.models import HistoricalRecords
from company.models import SystemSettings
from account.models import Account
from invoice.models import TransportPurchaseInvoice
from mandoob.models import mandoob_city

# Create your models here.
class TransportCompany(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    name_en = models.CharField(max_length=64, verbose_name=_("Company Name English"))
    name_ar = models.CharField(max_length=64, verbose_name=_("Company Name Arabic"))
    vat_no = models.CharField(max_length=64, verbose_name=_("VAT Number"), blank=True, null=True)
    history = HistoricalRecords(
        user_model='auth.User',
    )
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name=_("Account"), blank=True, null=True, editable=False)

    def __str__(self):
        if get_language() == "ar":
            return self.name_ar
        return self.name_en
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.account is None:
            parent_account = SystemSettings.objects.get(company=self.company).transport_company_account_tree
            account = Account(company=self.company, account_name_en=self.name_en, account_name_ar=self.name_ar, parent_account=parent_account, allow_edit=False, allow_child_accounts=False)
            account.save()
            self.account = account
            self.save()
        else:
            self.account.name_en = self.name_en
            self.account.name_ar = self.name_ar
            self.account.save()
        
        super().save(*args, **kwargs)


    
        
    

class TransportRoute(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    from_en = models.CharField(max_length=64, verbose_name=_("From English"))
    from_ar = models.CharField(max_length=64, verbose_name=_("From Arabic"))
    to_en = models.CharField(max_length=64, verbose_name=_("To English"))
    to_ar = models.CharField(max_length=64, verbose_name=_("To Arabic"))
    distance = models.IntegerField(verbose_name=_("Distance (km)"))

    is_linked_with_arrival_flight = models.BooleanField(default=False, verbose_name=_("Is linked with arrival flight"))
    is_linked_with_departure_flight = models.BooleanField(default=False, verbose_name=_("Is linked with departure flight"))

    from_linked_with_makkah_hotel = models.BooleanField(default=False, verbose_name=_("From linked with Makkah hotel"))
    to_linked_with_makkah_hotel = models.BooleanField(default=False, verbose_name=_("To linked with Makkah hotel"))
    from_linked_with_medina_hotel = models.BooleanField(default=False, verbose_name=_("From linked with Medina hotel"))
    to_linked_with_medina_hotel = models.BooleanField(default=False, verbose_name=_("To linked with Medina hotel"))
    history = HistoricalRecords(
        user_model='auth.User',
    )


    # For Mandoob
    mandoob_mark_as_completed = models.CharField(max_length=64, verbose_name=_("Mandoob who can Mark as completed"), choices = mandoob_city, blank=True, null=True)
    mandoob_mark_as_on_the_way = models.CharField(max_length=64, verbose_name=_("Mandoob who can Mark as on the way"), choices = mandoob_city, blank=True, null=True)
    


    def route_from(self):
        if get_language() == "ar":
            return self.from_ar
        return self.from_en
    
    def route_to(self):
        if get_language() == "ar":
            return self.to_ar
        return self.to_en
    
    def name_en(self):
        return f"{self.from_en} to {self.to_en}"
    
    def name_ar(self):
        return f"{self.from_ar} إلى {self.to_ar}"
    
    

    def __str__(self):
        if get_language() == "ar":
            return f"{self.from_ar} ← {self.to_ar}"
        return f"{self.from_en} → {self.to_en}"
    
    class Meta:
        unique_together = ['company', 'from_en', 'to_en']
        verbose_name = _("Transport Route")
        verbose_name_plural = _("Transport Routes")

class TransportType(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    name_en = models.CharField(max_length=64, verbose_name=_("Type Name English"))
    name_ar = models.CharField(max_length=64, verbose_name=_("Type Name Arabic"))
    capacity = models.IntegerField(verbose_name=_("Capacity"))
    show_in_transport_report = models.BooleanField(default=True, verbose_name=_("Show in transport report"))
    history = HistoricalRecords(
        user_model='auth.User',
    )



    def __str__(self):
        if get_language() == "ar":
            return self.name_ar
        return self.name_en
    
    class Meta:
        unique_together = ['company', 'name_en']
        verbose_name = _("Transport Type")
        verbose_name_plural = _("Transport Types")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class TransportMovement(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, null=True, blank=True)
    agent = models.ForeignKey('agent.Agent', on_delete=models.PROTECT, blank=True, null=True)
    voucher = models.ForeignKey('arrival_voucher.ArrivalVoucher', on_delete=models.PROTECT, blank=True, null=True)
    route = models.ForeignKey(TransportRoute, on_delete=models.PROTECT, verbose_name=_("Route"))
    type = models.ForeignKey(TransportType, on_delete=models.PROTECT, verbose_name=_("Type"), blank=True, null=True)
    date = models.DateField(verbose_name=_("Date"))
    time = models.TimeField(verbose_name=_("Time"))

    transport_company = models.ForeignKey(TransportCompany, on_delete=models.PROTECT, blank=True, null=True)
    # driver
    first_driver_name = models.CharField(max_length=64, verbose_name=_("Driver Name"), blank=True, null=True)
    first_driver_phone = models.CharField(max_length=64, verbose_name=_("Driver Phone"), blank=True, null=True)
    second_driver_name = models.CharField(max_length=64, verbose_name=_("Driver Name"), blank=True, null=True)
    second_driver_phone = models.CharField(max_length=64, verbose_name=_("Driver Phone"), blank=True, null=True)

    # hotel
    from_hotel = models.CharField(max_length=64, verbose_name=_("From Hotel"), blank=True, null=True)
    to_hotel = models.CharField(max_length=64, verbose_name=_("To Hotel"), blank=True, null=True)
    no_plate = models.CharField(max_length=64, verbose_name=_("No Plate"), blank=True, null=True)

    # invoice
    invoice = models.ForeignKey(TransportPurchaseInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name=_("Purchase Amount"), blank=True, null=True, default=0.00)
    sale_amount = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True, default=0.00)
    sale_invoice = models.ForeignKey('voucher.TransportInvoice', on_delete=models.SET_NULL, blank=True, null=True)
    # Status
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Rejected')),
        ('completed', _('Completed')),
        ('on_the_way', _('On the way')),
        ('delayed', _('Delayed')),
        ('date_open', _('Date Open')),

    ]
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"), blank=True, null=True)
    remarks = models.CharField(max_length=1028, verbose_name=_("Remarks"), blank=True, null=True)
    outside_package = models.BooleanField(default=False, verbose_name=_("Outside Package"))
    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        if get_language() == "ar":
            return f"{self.route.from_ar} - {self.route.to_ar} - {self.date} - {self.time}"
        return f"{self.route.from_en} - {self.route.to_en} - {self.date} - {self.time}"
    
    
    class Meta:
        unique_together = ['company', 'route', 'date', 'time']
        verbose_name = _("Transport Movement")
        verbose_name_plural = _("Transport Movements")


    def movement_from_hotel(self):
        if self.route.from_linked_with_makkah_hotel:
            return self.voucher.makkah_hotel
        elif self.route.from_linked_with_medina_hotel:
            return self.voucher.medina_hotel
        else:
            return None
        
    def movement_to_hotel(self):
        if self.route.to_linked_with_makkah_hotel:
            return self.voucher.makkah_hotel
        elif self.route.to_linked_with_medina_hotel:
            return self.voucher.medina_hotel
        else:
            return None
    
    def flight_no(self):
        if self.route.is_linked_with_arrival_flight:
            return self.voucher.arrival_flight_no
        elif self.route.is_linked_with_departure_flight:
            return self.voucher.departure_flight_no
        else:
            return None
    
    def show_on_tracking_screen(self):
        if self.status == 'confirmed':
            return True
        elif self.status == 'completed':
            return False
        elif self.status == 'on_the_way':
            return True
        elif self.status == 'delayed':
            return True
        else:
            return False
    
    def save(self, *args, **kwargs):
        if self.purchase_amount == None or self.purchase_amount < 0.00:
            self.purchase_amount = 0.00
        if self.sale_amount == None or self.sale_amount < 0.00:
            self.sale_amount = 0.00

        if self.id is None:
            self.voucher.accounts_status = 'pending'
            self.voucher.save()

        if self.outside_package == False and self.purchase_amount > 0.00:
            self.purchase_amount = 0.00
        
        if self.outside_package == False and self.sale_amount > 0.00:
            self.sale_amount = 0.00

        if self.outside_package == False:
            if self.invoice:
                self.invoice.delete()
                self.invoice = None
                self.purchase_amount = 0.00
            if self.sale_invoice:
                self.sale_invoice.delete()
                self.sale_invoice = None
                self.sale_amount = 0.00


            pass

    
            

            
        
                
        else:
            if self.invoice == None:
                invoice = TransportPurchaseInvoice()
                invoice.company = self.voucher.company
                invoice.transport_company = self.transport_company
                invoice.arrival_voucher = self.voucher
                invoice.date = self.date
                invoice.amount = self.purchase_amount
                invoice.additional_movement = True
                invoice.movement = self
                invoice.save()
                self.invoice = invoice
                pass
            else:
                
                invoice = TransportPurchaseInvoice.objects.get(pk=self.invoice.pk)
                invoice.company = self.voucher.company
                invoice.transport_company = self.transport_company
                invoice.arrival_voucher = self.voucher
                invoice.date = self.date
                invoice.amount = self.purchase_amount
                invoice.additional_movement = True
                invoice.movement = self
                invoice.save()
                self.invoice = invoice
                pass
            from voucher.models import TransportInvoice

            if self.sale_amount > 0.00: 
                if self.sale_invoice:
                    invoice = TransportInvoice.objects.get(pk=self.sale_invoice.pk)
                    invoice.company = self.voucher.company
                    invoice.agent = self.voucher.agent
                    invoice.date = self.date
                    invoice.voucher = self.voucher
                    invoice.transport_type = self.type or None
                    invoice.qty = 1
                    invoice.price = self.sale_amount
                    invoice.description = str('Transport Invoice, Voucher no. UP-' + str(self.pk) + ' Additional Movement: ' + str(self.route.name_en()) + " - "+'فاتورة النقل, رقم البرنامج UP-' + str(self.pk) + 'حركة إضافية: ' + str(self.route.name_ar()))
                    invoice.referance_no = self.voucher.agent_referance_no
                    invoice.additional_movement = True
                    invoice.movement = self
                    invoice.save()
                    self.sale_invoice = invoice
                    invoice.save()

                    
                else:
                    invoice = TransportInvoice()
                    invoice.company = self.voucher.company
                    invoice.agent = self.voucher.agent
                    invoice.date = self.date
                    invoice.voucher = self.voucher
                    invoice.transport_type = self.type or None
                    invoice.qty = 1
                    invoice.price = self.sale_amount
                    invoice.description = str('Transport Invoice, Voucher no. UP-' + str(self.pk) + ' Additional Movement: ' + str(self.route.name_en()) + 'فاتورة النقل, رقم البرنامج UP-' + str(self.pk) + 'حركة إضافية: ' + str(self.route.name_ar()))
                    invoice.referance_no = self.voucher.agent_referance_no
                    invoice.additional_movement = True
                    invoice.movement = self
                    invoice.save()
                    self.sale_invoice = invoice
                    invoice.save()
            
            else:
                if self.sale_invoice:
                    self.sale_invoice.delete()
                    self.sale_invoice = None
                else:
                    pass
                pass
            

        super().save(*args, **kwargs)


    def flight_date_differance(self):
        if self.route.is_linked_with_arrival_flight:
            d =  self.voucher.arrival_date
            print('Arrival Date: ', )
        elif self.route.is_linked_with_departure_flight:
            d =  self.voucher.departure_date
            print('Departure Date: ', )
        else:
            print('No flight')
    

    def delete(self, *args, **kwargs):
        if self.invoice:
            self.invoice.delete()
        else:
            pass
        super().delete(*args, **kwargs)



    # For Mandoob App
    def is_mandoob_allowed_to_mark_as_completed(self):
        if self.status == 'on_the_way':
            return True
        else:
            return False
        
    def is_mandoob_allowed_to_mark_as_on_the_way(self):
        if self.status == 'confirmed' or self.status == 'delayed' or self.status == 'pending':
            return True
        else:
            return False
    

    def is_edit_allowed(self):
        if self.status == 'completed' or self.status == 'date_open':
            return False
        else:
            return True
        
    def is_delete_allowed(self, user):
        if user.has_perm('transport.delete_transportmovement'):
            return True
        else:
            return False
        

        


        
    
class TransportPackage(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT)
    package_name_en = models.CharField(max_length=128, verbose_name=_("Package Name English"))
    package_name_ar = models.CharField(max_length=128, verbose_name=_("Package Name Arabic"))
    package_short_code = models.CharField(max_length=64, verbose_name=_("Package Short Code"), blank=True, null=True)
    routes = models.ManyToManyField(TransportRoute, verbose_name=_("Routes"))
    history = HistoricalRecords(
        user_model='auth.User',
    )
    def __str__(self):
        if get_language() == "ar":
            return self.package_name_ar
        return self.package_name_en
    class Meta:
        unique_together = ['company', 'package_name_en']
        verbose_name = _("Transport Package")
        verbose_name_plural = _("Transport Packages")


    def total_routes(self):
        return self.routes.count()