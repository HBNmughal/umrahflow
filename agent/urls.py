"""umrahpro URL Configuration

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
from agent.views import *
from django.urls import path, include
from .htmx import *
urlpatterns = [
    path('', agent_dashboard, name="agent_dashboard"),

    path('agent_list/', agent_list, name="agent_list"),
    path('agent_list/add/', add_agent, name="add_agent"),
    path('agent_list/edit/<int:pk>/', edit_agent, name="edit_agent"),
    path('agent_list/edit/<int:pk>/price/', agent_price_list, name="agent_price_list"),
    path('agent_list/edit/<int:pk>/comission/', agent_commission_form, name="agent_commission_form"),

    path('agent_list/edit/<int:pk>/agent_code_form/', agent_code_form, name="agent_code_form"),
    path('agent_list/edit/<int:pk>/user/create/', create_agent_user, name="create_agent_user"),
    path('agent_list/edit/<int:pk>/user/edit/', edit_agent_user, name="edit_agent_user"),
    path('get_agent_price/', get_agent_price, name='get_agent_price'),




    path('agent_list/add_external_agent/', add_agent_external, name="add_external_agent"),

    path('account/', agent_account_view, name="agent_account_view"),

    path('arrival_vouchers/', arrival_vouchers_list_htmx, name="agent_arrival_vouchers_list"),
    path('arrival_vouchers/<int:pk>/', agent_arrival_voucher, name='agent_arrival_voucher'),
    path('arrival_vouchers/<int:pk>/submit/', submit_arrival_voucher, name='agent_submit_arrival_voucher'),
    path('arrival_vouchers/add/', add_arrival_voucher, name="agent_add_arrival_voucher"),
    path('operating_schedule/<day>/', agent_operating_schedule, name="agent_operating_schedule"),
    path('arrival_vouchers/<int:pk>/print/', agent_arrival_voucher_print , name='agent_arrival_voucher_print'),


    
    # 
    path('htmx/search_arrival_vouchers/', search_view, name='agent_voucher_search_view'),

]


