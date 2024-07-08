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
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from .views import *
from .htmx import *
urlpatterns = (
   
    # Arrival Voucher Invoice Pending
    path('pending_arrival_voucher_invoice_list/', pending_arrival_voucher_invoice_list, name='pending_arrival_voucher_invoice_list'),
    path('approved_arrival_voucher_invoice_list/', approved_arrival_voucher_invoice_list, name='approved_arrival_voucher_invoice_list'),
    path('pending_arrival_voucher_invoice/<voucher_id>/', arrival_voucher_invoice, name='arrival_voucher_invoice'),
    path('pending_arrival_voucher_invoice_list/htmx/',pending_arrival_voucher_invoice_list_htmx , name='pending_arrival_voucher_invoice_list_htmx'),
    path('approved_arrival_voucher_invoice_list/htmx/',approved_arrival_voucher_invoice_list_htmx , name='approved_arrival_voucher_invoice_list_htmx'),
    

)
