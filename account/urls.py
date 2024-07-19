from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.accounts_settings_form, name='accounts_settings_form'),
    path('list/', views.account_list_view, name='account-list'),
    path('create/<pk>/sub_account/', views.create_account, name='account_create_sub_account'),
    path('edit/<pk>/sub_account/', views.edit_account, name='edit_sub_account'),
    path('transport_company_account_list/', views.transport_company_account_list_view, name='transport_company_account_list'),
    path('account_view/<pk>/', views.account_view, name='account_view'),
    path('print_receipt_voucher/<pk>/', views.print_receipt_voucher, name='print_receipt_voucher'),
    path('print_debit_voucher/<pk>/', views.print_debit_voucher, name='print_debit_voucher'),
    path('print_account_statement/<pk>/', views.print_account_statement, name='print_account_statement'),

    path('transaction_list/', views.transaction_list_view, name='transaction_list_view'),
    path('transaction_view/<pk>/', views.transaction_view, name='transaction_view'),

    path('receipt_voucher_list/', views.receipt_voucher_list_view, name='receipt_voucher_list_view'),
    path('receipt_voucher_view/<pk>/', views.receipt_voucher_view, name='receipt_voucher_view'),
    path('receipt_voucher_add/', views.receipt_voucher_add_view, name='receipt_voucher_add_view'),
    path('receipt_voucher_edit/<pk>/', views.receipt_voucher_edit_view, name='receipt_voucher_edit_view'),
    path('receipt_voucher_print/<pk>/', views.receipt_voucher_print, name='receipt_voucher_print'),


    path('payment_voucher_list/', views.payment_voucher_list_view, name='payment_voucher_list_view'),
    path('payment_voucher_view/<pk>/', views.payment_voucher_view, name='payment_voucher_view'),
    path('payment_voucher_add/', views.payment_voucher_add_view, name='payment_voucher_add_view'),
    path('payment_voucher_edit/<pk>/', views.payment_voucher_edit_view, name='payment_voucher_edit_view'),
    path('payment_voucher_print/<pk>/', views.payment_voucher_print, name='payment_voucher_print'),
    path('test/', views.tempelate_test, name='test'),
    path('create-transaction/', views.create_transaction, name='create_transaction'),


    path('agents_accounts_view/<str:agent_type>/', views.agents_accounts_view, name='agents_accounts_view'),
    
]

