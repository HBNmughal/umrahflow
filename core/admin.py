from django.contrib import admin
from .models import Country
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

admin.site.register(Country, SimpleHistoryAdmin)