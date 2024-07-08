from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from .models import *
from django.utils.translation import gettext_lazy as _, get_language
# get language
from django.utils import translation

class PermissionAjaxDatatableView(AjaxDatatableView):

    model = Permission
    title = 'Permissions'
    initial_order = [["app_label", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'codename', 'visible': True, },
        {'name': 'name', 'visible': True, },
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]
def get_agent_name():
    if get_language() == 'en':
        return 'agent__name_en'
    elif get_language() == 'ar':
        return 'agent__name_ar'
class AgentVoucherAjaxDatatableView(AjaxDatatableView):
    def get_agent_name():
        if get_language() == 'en':
            return 'agent__name_en'
        elif get_language() == 'ar':
            return 'agent__name_ar'
    model = AgentVoucher
    title = 'Agent Voucher'
    initial_order = ["date", "desc"],
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
    def get_initial_queryset(self, request=None):
        queryset = AgentVoucher.objects.filter(company=request.user.employee.company)
        return queryset
    
    def render_column(self, row, column):
        if column == 'total':
            return row.total()
        return super(AgentVoucherAjaxDatatableView, self).render_column(row, column)


    
    

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id',"title": "#", 'visible': True, "searchable": False },
        {'name': 'agent__name_en', 'foreign_field':'agent__name_en', 'visible': True, 'title': ('Agent')},
        {'name': 'agent__name__ar', 'foreign_field':'agent__name_ar', 'visible': True, 'title': ('الوكيل')},

        {'name': 'date', 'visible': True, },
        {'name': 'voucher_no', 'visible': True, },
        {'name': 'group_no', 'visible': True, },
        {'name': 'pax', 'visible': True, },
        {'name': 'sale_price',"title": _("Sale Price"), 'visible': True, },   
        {'name': 'total',"title": _("Total"), 'visible': True, },   
        {'name': 'action','title' : _('Action') , 'visible': True, 'searchable': False},

    ]


    def customize_row(self, row, obj):
        row['action'] = """ 
        <a onclick="popupCenter({url: '%s/edit/', title: 'xtf', w: 900, h: 900});" class="btn btn-link btn-sm"><i class="fe fe-edit fe-16" aria-hidden="true"></i></a>
        <a onclick="popupCenter({url: '%s/print/', title: 'xtf', w: 900, h: 900});" class="btn btn-link btn-sm"><i class="fe fe-printer fe-16" aria-hidden="true"></i></a>
        """ %(obj.id, obj.id)

        row['agent'] = """
        {obj.agent} ({obj.agent.country})

        """ .format(obj=obj)

        row['date'] = """
        {date}

        """ .format(date=obj.date.strftime('%d/%m/%Y'))
