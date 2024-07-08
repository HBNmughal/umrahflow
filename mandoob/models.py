from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import base64
# Create your models here.

mandoob_city = (
    ('makkah', _('Makkah')),
    ('madinah', _('Medina')),
    ('medina_airport', _('Medina Airport')),
    ('jeddah_airport', _('Jeddah Airport')),
)





class Mandoob(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name=_('Company'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    city = models.CharField(max_length=20, choices=mandoob_city, verbose_name=_('City'))
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    username = models.CharField(max_length=100, verbose_name=_('Username'))
    password = models.CharField(max_length=100, verbose_name=_('Password'))
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name=_('User'))
    token = models.CharField(max_length=64, verbose_name=_("Token"), blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Mandoob')
        verbose_name_plural = _('Mandoobs')
        permissions = (
            ('view_jeddah_airport_schedule', _('View Jeddah Airport Schedule')),
            ('view_medina_airport_schedule', _('View Medina Airport Schedule')),
            ('view_makkah_schedule', _('View Makkah Schedule')),
            ('view_madinah_schedule', _('View Madinah Schedule')),
            ('can_update_group_leader', _('Can Update Group Leader')),
            ('can_update_makkah_hotel', _('Can Update Makkah Hotel')),
            ('can_update_madinah_hotel', _('Can Update Madinah Hotel')),
            ('can_mark_as_completed', _('Can Mark As Completed')),
            ('can_mark_as_on_the_way', _('Can Mark As On The Way')),
        )


    def save(self, *args, **kwargs):

        if self.id:
            print("id available")
            user = User.objects.get(pk=self.user.pk)
            user.username = self.username
            user.set_password(self.password)
            user.save()
            
        else:
            print("id not available")
            user = User.objects.create_user(username=self.username, password=self.password)
            self.user = user
            
        
        
        if self.user:
            if self.token:
                print("token available")
            else:
                print("token not available")
                self.token = (base64.b32encode(bytearray('umrahpro'+str(str(self.company.permit_no)+str(self.id)), 'ascii')).decode('utf-8')).replace('=', '')
        super().save(*args, **kwargs)


    

