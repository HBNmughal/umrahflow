from django.contrib import admin
from .models import Company, Employee, Designation, CompanyEmail, SystemSettings
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(Designation, SimpleHistoryAdmin)
admin.site.register(CompanyEmail, SimpleHistoryAdmin)
admin.site.register(SystemSettings, SimpleHistoryAdmin)
admin.site.site_header = "UmrahFlow Admin"
admin.site.site_title = "UmrahFlow Admin Portal"
admin.site.index_title = "Welcome to UmrahFlow Portal"


