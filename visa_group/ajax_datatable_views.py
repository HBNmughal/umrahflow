from django.urls import reverse
from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from .models import UmrahVisaGroupInvoice
from django.utils.translation import gettext_lazy as _, get_language
# get language
from django.utils import translation
def get_agent_name():
    if get_language() == 'en':
        return 'agent__name_en'
    elif get_language() == 'ar':
        return 'agent__name_ar'
class UmrahVisaGroupInvoiceAjaxDatatableView(AjaxDatatableView):
    def get_agent_name():
        if get_language() == 'en':
            return 'agent__name_en'
        elif get_language() == 'ar':
            return 'agent__name_ar'
    model = UmrahVisaGroupInvoice
    title = 'Agent Voucher'
    initial_order = ["date", "desc"],
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
    def get_initial_queryset(self, request=None):
        queryset = UmrahVisaGroupInvoice.objects.filter(company=request.user.employee.company)
        return queryset
    
    def render_column(self, row, column):
        if column == 'total_visa_price':
            return row.total_visa_price()
        return super(UmrahVisaGroupInvoiceAjaxDatatableView, self).render_column(row, column)


    
    def agent_name():
        if get_language() == 'en':
            return {'name': 'agent__name_en', 'foreign_field':'agent__name_en', 'visible': True, 'title': ('Agent')}
        elif get_language() == 'ar':
            return {'name': 'agent__name_ar', 'foreign_field':'agent__name_ar', 'visible': True, 'title': ('الوكيل')}

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id',"title": "#", 'visible': True, "searchable": False },
        {'name': 'agent__name_en', 'foreign_field':'agent__name_en', 'visible': True, 'title': ('Agent')},
        {'name': 'agent__name__ar', 'foreign_field':'agent__name_ar', 'visible': True, 'title': ('الوكيل')},

        {'name': 'date', 'visible': True, },
        {'name': 'voucher_no', 'visible': True, },
        {'name': 'group_no', 'visible': True, },
        {'name': 'pax', 'visible': True, },
        {'name': 'visa_sale_price',"title": _("Sale Price"), 'visible': True, },
        {'name': 'transport_included',"title": _("Transport Included"), 'visible': True,},
        {'name': 'total_visa_price',"title": _("Total"), 'visible': True, },   
        {'name': 'action','title' : _('Action') , 'visible': True, 'searchable': False},

    ]


    def customize_row(self, row, obj):
        row['action'] = """
        <a href="{edit_url}" class="btn btn-primary  btn-sm"><i class="fe fe-edit"></i></a>
        <a href="{transaction_url}" class="btn btn-warning btn-sm"><i class="fe fe-repeat"></i></a>
        
        """.format(edit_url=reverse('umrah_visa_group_invoice_edit', args=[obj.pk]), edit_title=_('Edit'), transaction_url=reverse('transaction_view', args=[obj.transaction.pk if obj.transaction else "0"]), transaction_title=_('Transaction'))
        row['agent'] = """
        {obj.agent} ({obj.agent.country})

        """ .format(obj=obj)

        row['date'] = """
        {date}

        """ .format(date=obj.date.strftime('%d/%m/%Y'))
        row['transport_included'] = """
        {transport_included}

        """ .format(transport_included=_("Yes") if obj.transport_included else _("No"))
