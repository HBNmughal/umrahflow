
from transport.views import *
from django.urls import path

urlpatterns = [
    path('transport_routes/', transport_routes, name="transport_routes"),
    path('transport_routes/add/', add_transport_route, name="add_transport_route"),
    path('transport_routes/<int:route_id>/edit', edit_transport_route, name="edit_transport_route"),



    
    # path('transport_routes/<route_id>/edit/', edit_transport_route, name="edit_transport_route"),
    # path('transport_routes/<route_id>/delete/', delete_transport_route, name="delete_transport_route"),
    path('transport_company_add/', transport_company_add, name="transport_company_add"),
    path('edit_transport_company/<int:pk>/', edit_transport_company, name="edit_transport_company"),


    path('transport_packages/', transport_package_list, name="transport_packages"),
    path('transport_packages/add/', transport_package_form, name="transport_package_add"),
    
    path('transport_packages/<int:pk>/edit/', transport_package_form, name="transport_package_edit"),

]