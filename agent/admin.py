from django.contrib import admin
from .models import Agent, AgentPrice, AgentCode, AgentCommission
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Agent, SimpleHistoryAdmin)
admin.site.register(AgentPrice, SimpleHistoryAdmin)
admin.site.register(AgentCode)
admin.site.register(AgentCommission, SimpleHistoryAdmin)


