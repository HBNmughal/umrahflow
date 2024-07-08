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
from core.views import *
from core.htmx_lookups import *
from .barcode import generate_barcode
from django.urls import path, include
urlpatterns = [
    path('', home, name="dashboard"),
    path('login/', login_form, name="login"),
    path('logout/', logout_button, name="logout"),
    path('apps/', apps, name="apps"),
    path('app_select/<app>/', select_app, name="app_select"),
    path('mandoob/', include('mandoob.urls')),
    # htmx lookups here
    path('htmx/get_agent_sale_price', get_agent_sale_price, name="get_agent_sale_price"),


    path('media/barcode/<barcode_data>/', generate_barcode, name='generate_barcode'),
]


