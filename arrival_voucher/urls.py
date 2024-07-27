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
from .test_htmx import *
urlpatterns = (
    path(_('admin/'), admin.site.urls),


    #Voucher
    path('arrival_vouchers/', arrival_voucher_list, name='arrival_voucher_list'),
    path('arrival_vouchers/htmx/', arrival_vouchers_list_htmx, name='arrival_vouchers_list_htmx'),

    path('arrival_vouchers/add/', add_arrival_voucher, name='add_arrival_voucher'),
    path('arrival_vouchers/<int:pk>/', arrival_voucher, name='arrival_voucher'),
    path('arrival_vouchers/<int:pk>/submit/',arrival_voucher_submit , name='arrival_voucher_submit'),
    path('arrival_vouchers/<int:pk>/print/', arrival_voucher_print , name='arrival_voucher_print'),
    path('arrival_vouchers/<int:pk>/approval_form/', voucher_approval_form , name='voucher_approval_form'),





    # Voucher Edit Forms
    path('arrival_vouchers/<pk>/group/edit/', arrival_voucher_group_details_form, name='arrival_voucher_group_details_form'),
    path('arrival_vouchers/<pk>/flight/edit/', arrival_voucher_flight_details_form, name='arrival_voucher_flight_details_form'),
    path('arrival_vouchers/<pk>/accommodation/edit/', arrival_voucher_accommodation_details_form, name='arrival_voucher_accommodation_details_form'),
    path('arrival_vouchers/<pk>/transport/edit/', transport_brn_form, name='transport_brn_form'),
    path('arrival_vouchers/<voucher_id>/transport/add/', transport_movement_formset, name='transport_movement_formset'),
    


    # Schedule
    path('operating_schedule/<day>/', operating_schedule, name='operating_schedule'),
    path('operating_schedule/<day>/print', print_operating_schedule, name='print_operating_schedule'),

    path('schedule/<int:movement_id>/edit/driver/', assign_driver, name='assign_driver'),
    path('schedule/<int:movement_id>/edit/assign_group_leader/', assign_group_leader, name='assign_group_leader'),
    path('schedule/<int:movement_id>/edit/status/', status_change, name='movement_status_form'),
    path('schedule/<int:movement_id>/edit/status/table/', status_change_table, name='movement_status_change_table'),
    path('schedule/<int:voucher_id>/voucher_movement_history/', voucher_movement_history, name='voucher_movement_history'),




    # Operating Schedule Tracking Screen
    path('schedule_tracking_screen/<str:key>/', schedule_tracking_screen, name='schedule_tracking_screen'),
    path('schedule_tracking_screen/<str:key>/<str:content>/', schedule_tracking_screen, name='schedule_tracking_screen_content'),



    # rawdah
    path('rawdah_permit_list/', rawdah_permit_list, name='rawdah_permit_list'),
    path('rawdah_permit_list/add', add_rawdah_permit, name='add_rawdah_permit'),
    path('rawdah_permit_list/<int:pk>/', edit_rawdah_permit, name='edit_rawdah_permit'),

    path('test/htmx/search_view/', search_view, name='search_view'),
    path('trips_date_open/', trips_date_open, name='trips_date_open'),

    
    

)
