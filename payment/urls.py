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
from payment.views import *
from django.urls import path, include
urlpatterns = [
    path('agent_list/', payments_agents_list, name="payments_agents_list"),
    path('agent_list/agents_current_balance_print/', agents_current_balance_print, name="agents_current_balance_print"),
    path('payment_account/<agent_type>/<agent_id>', agent_account_view, name="agent_account_view"),
    path('payment_account/<agent_id>/print_agent_reciept_voucher_report/', print_agent_reciept_voucher_report, name="print_agent_reciept_voucher_report"),
    path('payment_account/<agent_id>/print_agent_transactions/', print_agent_account_statement, name="print_agent_account_statement"),
    path('payment_account/print_all_agents_reciept_voucher_report/', print_all_agents_reciept_voucher_report, name="print_all_agents_reciept_voucher_report"),

    path('payment_account/<agent_type>/<agent_id>/collect/', collect_payment, name="collect_payment"),
    path('payment_account/<agent_type>/<agent_id>/withdraw/', withdraw_payment, name="withdraw_payment"),
    # edit payment
    path('payment_account/<agent_id>/collect/<transaction_id>/edit/', edit_collect_payment, name="edit_collect_payment"),
    path('payment_account/agent_transactions/delete/', delete_collect_payment, name="delete_collect_payment"),
    path('payment_account/<agent_type>/<agent_id>/collect/<transaction_id>/print/', print_receipt_voucher, name="print_receipt_voucher"),
    
    # Settlements
    path('payment_account/<agent_id>/credit/', agent_settlement_credit, name="agent_settlement_credit"),
    path('payment_account/<agent_id>/debit/', agent_settlement_debit, name="agent_settlement_debit"),
    path('payment_account/<agent_id>/<transaction_id>/<type>/edit/', edit_agent_settlement, name="edit_agent_settlement"),


    path('office_expense/', office_expenses_list, name="office_expenses_list"),

    path('office_expense/add/', office_expense_form, name="office_expense_form"),
    path('office_expense/<transaction_id>/print/', print_withdrawl_voucher_office, name="print_withdrawl_voucher_office"),


    path('treasury/', treasury, name="treasury"),
    path('treasury/collect/', treasury_collect_payment, name="treasury_collect_payment"),
    path('treasury/treasury_report/', treasury_report, name="treasury_report"),


    path('payrolls/', payroll_list, name="payrolls"),
    path('payrolls/create/', payroll_form, name="create_payroll"),
    path('payrolls/<payroll_id>/', view_payroll, name="view_payroll"),

    path('payrolls/<payroll_id>/<employee>/print', print_payslip, name="print_payslip"),
    path('payrolls/<payroll_id>/<employee>/salary_collected', salary_collected, name="salary_collected"),
    
    path('account_list/', account_list, name="demo_account_list"),
    path('account_list/add/', account_form, name="demo_account_form"),
    # path('account_list/<account_id>/', account_view, name="demo_account_view"),
    path('account_list/<account_id>/edit/', edit_account, name="demo_account_form"),
    # path('account_list/<account_id>/credit/', account_credit_form, name="demo_account_credit_form"),
    # settlement
    path('account_list/<account_id>/settlement_credit/', account_settlement_credit, name="demo_account_settlement_credit"),
    path('account_list/<account_id>/settlement_debit/', account_settlement_debit, name="demo_account_settlement_debit"),
    # path('account_list/<account_id>/debit/', account_debit_form, name="demo_account_debit_form"),
    # path('account_list/<account_id>/account_transfer_form/', account_transfer_form, name="demo_account_transfer_form"),
    # path('account_list/<account_id>/<transaction_id>/print/', print_account_transaction, name="demo_print_account_transaction"),
    





]


