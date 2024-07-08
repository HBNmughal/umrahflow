from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
admin.site.register(TransportCompany, SimpleHistoryAdmin)
admin.site.register(TransportRoute, SimpleHistoryAdmin)
admin.site.register(TransportType, SimpleHistoryAdmin)
admin.site.register(TransportMovement, SimpleHistoryAdmin)
admin.site.register(TransportPackage, SimpleHistoryAdmin)

