from django.db import models
from django.utils.translation import gettext as _, get_language
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save
# from django_otp.models import Device

class Country(models.Model):
    name_en = models.CharField(max_length=32, verbose_name=_("Country name english"))
    name_ar = models.CharField(max_length=32, verbose_name=_("Country name arabic"))
    code = models.IntegerField(verbose_name=_("Country phone code"))

    history = HistoricalRecords(
        user_model='auth.User',
    )


    def __str__(self):
        if get_language() == 'ar':
            return self.name_ar
        return self.name_en



# class EmailDevice(Device):
#     token = models.CharField(max_length=6, blank=True, null=True)

#     def generate_token(self):
#         self.token = f'{random.randint(100000, 999999):06}'
#         self.save()

#     def verify_token(self, token):
#         return self.token == token