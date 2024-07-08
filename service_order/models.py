from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import *
# Create your models here.

class ServiceOrder(models.Model):
    company = models.ForeignKey("company.Company", verbose_name=_("Company"), on_delete=models.CASCADE)
    agent = models.ForeignKey("agent.Agent", verbose_name=_("Agent"), on_delete=models.CASCADE)
    arrival_type = models.CharField(_("Arrival Type"), max_length=50, choices=arrival_types)
    pax = models.IntegerField(_("PAX"))
    group_leader_name = models.CharField(_("Group Leader Name"), max_length=50)
    group_leader_mobile = models.CharField(_("Group Leader Mobile"), max_length=50)



    #arrival
    arrival_date = models.DateField(_("Arrival Date"), auto_now=False, auto_now_add=False)
    arrival_time = models.TimeField(_("Arrival Time"), auto_now=False, auto_now_add=False)
    arrival_flight_no = models.CharField(_("Arrival Flight No"), max_length=50, blank=True, null=True)
    arrival_port =models.CharField(_("Arrival Port"), max_length=50, blank=True, null=True)
    arrival_to = models.CharField(_("Arrival to"), max_length=50, blank=True, null=True)

    #departure
    departure_date = models.DateField(_("Departure Date"), auto_now=False, auto_now_add=False)
    departure_time = models.TimeField(_("Departure Time"), auto_now=False, auto_now_add=False)
    departure_flight_no = models.CharField(_("Departure Flight No"), max_length=50, blank=True, null=True)
    departure_port =models.CharField(_("Departure Port"), max_length=50, blank=True, null=True)
    departure_to = models.CharField(_("Departure from"), max_length=50, blank=True, null=True)
    


    #hotel
    makkah_hotel = models.CharField(_("Makkah Hotel"), max_length=50, blank=True, null=True)
    medina_hotel = models.CharField(_("Medina Hotel"), max_length=50, blank=True, null=True)


    status = models.CharField(_("Status"), max_length=50, choices=service_order_status)
    status_remarks = models.CharField(_("Status Remarks"), max_length=50)

    class Meta:
        verbose_name = _('Service Order')
        verbose_name_plural = _('Service Orders')