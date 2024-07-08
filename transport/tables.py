import django_tables2 as tables
from .models import TransportRoute, TransportMovement, TransportPackage
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class TransportRouteTable(tables.Table):
    class Meta:
        model = TransportRoute
        template_name = "django_tables2/bootstrap_custom.html"
        fields = ['from_en', 'from_ar', 'to_en', 'to_ar', 'distance']

        attrs = {'class': 'table table-hover table-striped table-bordered'}
        empty_text = "No Transport Routes Found"
        orderable = True

class TransportPackageTable(tables.Table):
    total_routes = tables.Column(empty_values=(), verbose_name=_('Total Routes'), orderable=False)

    edit_button = tables.Column(empty_values=(), verbose_name=_('Edit'), orderable=False)
    
    class Meta:
        model = TransportPackage
        template_name = "django_tables2/bootstrap_custom.html"
        fields = ['package_name_en', 'package_name_ar']
        attrs = {'class': 'table table-hover table-striped table-bordered'}
        empty_text = "No Transport Packages Found"

    
    def render_total_routes(self, record):
        return record.routes.count()

    # CREATE EDIT BUTTON
    def render_edit_button(self, record):
        return format_html(
        """<a href="" class="btn btn-primary" onClick="popupCenter({{url: '{}', title: 'xtf', w: 900, h: 900}});">{}</a>""",
        reverse('transport_package_edit', args=[record.pk]),
        _('Edit')
    )

