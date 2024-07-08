"""umrahflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home
from voucher.views import *
from core.views import *
from django.urls import path, include
from . import ajax_datatable_views

urlpatterns = [
    # path('', home, name="dashboard"),
    path('sub_agent_voucher/', sub_agent_voucher_list, name="sub_agent_voucher_list"),

    path('<type>/add/', add_new_voucher, name="add_new_voucher"),
    path('<type>/<voucher_id>/edit/', edit_voucher, name="edit_voucher"),
    path('<type>/<voucher_id>/print/', print_voucher, name="print_voucher"),


    path('initial_voucher_price/', initial_voucher_price, name="initial_voucher_price"),
    path('report/vouchers/<agent_type>/', print_voucher_list, name="print_voucher_list"),
    path('delete_voucher/', delete_voucher, name='delete_voucher'),
    

    path('transport_invoice_list/', transport_invoice_list, name="transport_invoice_list"),
    path('add_transport_invoice/', add_transport_invoice, name="add_transport_invoice"),
    path('edit_transport_invoice/<invoice_id>/', edit_transport_invoice, name="edit_transport_invoice"),
    path('delete_transport_invoice/', delete_transport_invoice, name="delete_transport_invoice"),


    path('ajax_datatable/permissions/', ajax_datatable_views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path('ajax_datatable/agent_voucher/', ajax_datatable_views.AgentVoucherAjaxDatatableView.as_view(), name="ajax_datatable_agent_voucher"),


]
