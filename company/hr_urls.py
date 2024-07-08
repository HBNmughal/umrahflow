
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
from company.views import *
from mandoob.views import *
from django.urls import path, include
urlpatterns = [
    # path('', home, name="dashboard"),
    path('designations/', designations, name="designations"),
    path('designations/add/', add_designation, name="add_designation"),


    path('employees/', employees, name="employees"),
    path('employees/add/', add_employee, name="add_employee"),
    path('employees/edit/<pk>', edit_employee, name="edit_employee"),


    path('mandoobs/', mandoobs, name="mandoobs"),
    path('mandoobs/add/', add_mandoob, name="add_mandoob"),
    path('mandoobs/edit/<pk>', edit_mandoob, name="edit_mandoob"),




    


]
