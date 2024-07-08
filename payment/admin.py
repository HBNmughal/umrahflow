from django.contrib import admin
from .models import AgentPaymentTransaction, OfficeExpense, CompanyTreasuryTransaction, Payroll,EmployeeSalary
# Register your models here.
admin.site.register(AgentPaymentTransaction)
admin.site.register(OfficeExpense)
admin.site.register(CompanyTreasuryTransaction)
admin.site.register(Payroll)
admin.site.register(EmployeeSalary)




