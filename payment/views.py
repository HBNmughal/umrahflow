from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.db.models import Sum
from num2words import num2words
from core.token_auth import verify_auth_key
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from django.shortcuts import render
from company.models import Company, Employee
from agent.models import Agent
from payment.models import AgentPaymentTransaction, OfficeExpense, CompanyTreasuryTransaction, Payroll, EmployeeSalary

from payment.forms import (AgentCollectPayment, AgentWithdrawPayment, OfficeExpenseForm, TreasuryCollectPayment, PayrollForm, AgentSettlementTransactionCreditForm, AgentSettlementTransactionDebitForm,


)

from django.contrib import messages 
from django.utils.translation import gettext_lazy as _
from voucher.models import AgentVoucher
import datetime

# Create your views here.



def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)






@login_required()
def payments_agents_list(request):
    company = request.user.employee.company
    agents = Agent.objects.filter(company = company)
    _company = Company.objects.get(id=request.user.employee.company.id)

    agents_credit = 0.00
    agents_debit = 0.00


    for agent in agents:
        if agent.account_balance() > 0.00:
            agents_credit += agent.account_balance()
        elif agent.account_balance() < 0.00:
            agents_debit += agent.account_balance()
        else:
            pass

        
        






    context = {
        "agents": agents,
        "company": _company,
        "agents_credit": agents_credit,
        "agents_debit": agents_debit,

  


    }
    return render(request, "payment_agent_list.html", context)

# @login_required()
# def agent_account_view(request, agent_type, agent_id):
#     agent = Agent.objects.get(company=request.user.employee.company.id, id=agent_id)
#     main_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['c', 'd']).order_by('date', 'time')  
#     balance = 0.00
#     transactions = []
#     for t in main_transactions:
#         if t.transaction_type == "c":
#             balance += float(t.amount)
#         elif t.transaction_type == "d":
#             balance -= float(t.amount)
#         else:
#             pass
#         t.balance = balance
#         transactions.append({
#             "transaction": t,
#             "balance": balance
#         })


    
#     context = {
#         "agent" : agent,
#         # "transactions": main_transactions,
#         "agent_type": agent_type,
#         "transactions": transactions
        
#     }
#     return render(request, "agent_account_view.html", context)

@permission_required('payments.add_agentpaymenttransaction',raise_exception=True)
def collect_payment(request, agent_type, agent_id):
    form = AgentCollectPayment()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['agent'].initial = agent_id
    form.fields['performed_by'].initial = request.user.employee.name
    form.fields['transaction_type'].initial = 'c'
    if request.method == 'POST':
        if request.method == 'POST':
            form = AgentCollectPayment(request.POST)
            if form.is_valid():
                if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    messages.success(request, _('Payment Collected Succesfully'))
                    return render(request, "close_popup.html")
                else: 

                    context = {
                        "form": form,
                        'otp_error': _("Wrong token")
                    }

                    return render(request, "popup_forms/collect_payment.html", context)
    context = {
        "form": form,
    }

    return render(request, "popup_forms/collect_payment.html", context)
@permission_required('payments.add_agentpaymenttransaction',raise_exception=True)   
def edit_collect_payment(request, agent_id ,transaction_id):
    transaction = AgentPaymentTransaction.objects.get(company=request.user.employee.company, agent = Agent.objects.get(id=agent_id), id=transaction_id)
    form = AgentCollectPayment(instance=transaction)
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['agent'].initial = agent_id
    form.fields['performed_by'].initial = request.user.employee.name
    form.fields['transaction_type'].initial = 'c'
    if request.method == 'POST':
        if request.method == 'POST':
            form = AgentCollectPayment(request.POST, instance=transaction)
            if form.is_valid():
                if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    messages.success(request, _('Payment Collected Succesfully'))
                    return render(request, "close_popup.html")
                else: 

                    context = {
                        "transaction": transaction,

                        "form": form,
                        'otp_error': _("Wrong token")
                    }
                    return render(request, "popup_forms/collect_payment.html", context)
    context = {
        "transaction": transaction,
        "form": form,
    }

    return render(request, "popup_forms/collect_payment.html", context)

@permission_required('payment.delete_agentpaymenttransaction',raise_exception=True)
def delete_collect_payment(request):
    if request.method == 'POST':
        transaction = AgentPaymentTransaction.objects.get(company=request.user.employee.company, id=request.POST.get('transaction_id'))
        transaction.delete()
        messages.success(request, _('Payment has been deleted succesfully'))
        return render(request, "close_popup.html")
    else:
        return HttpResponse("Invalid Request")





@permission_required('payment.add_agentpaymenttransaction',raise_exception=True)
def withdraw_payment(request, agent_type, agent_id):
    agent = Agent.objects.get(id=agent_id)
    form = AgentWithdrawPayment()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['agent'].initial = agent_id
    form.fields['performed_by'].initial = request.user.employee.name
    form.fields['reason'].initial = "1"
    if request.method == 'POST':
        form = AgentWithdrawPayment(request.POST)
        if form.is_valid():
            form.cleaned_data['reason'] = _("Withdraw")
            _save = form.save(commit=False)
            if _save.transaction_type == "d":
                _save.reason = _("Withdraw from Account Balance")
            elif _save.transaction_type == "cod":
                _save.reason = _("Commission Withdrawl")
            elif _save.transaction_type == "rd":
                _save.reason = _("Returns Withdrawl")
            else:
                pass

            _save.save()
            messages.success(request, _('Payment Withdraw has been made succesfully'))
            return render(request, "close_popup.html")
        else:
            context = {
                "form": form,
                "agent": agent
            }
            return render(request, "popup_forms/withdraw_payment.html", context)

    context = {
        "form": form,
        "agent": agent
    }

    return render(request, "popup_forms/withdraw_payment.html", context)

@login_required()
def print_receipt_voucher(request, agent_type, agent_id, transaction_id):
    transaction = AgentPaymentTransaction.objects.get(company=request.user.employee.company, agent = Agent.objects.get(id=agent_id), id=transaction_id)
    context = {
        "transaction": transaction

    }
    if transaction.transaction_type in ['d', 'cod', 'rd']:
        return render(request, "print/withdraw_receipt.html", context)
    elif transaction.transaction_type in ['c', 'co', 'r']:
        return render(request, "print/receipt_voucher.html", context)


@login_required()
def office_expense_form(request):
    form = OfficeExpenseForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['accountant'].initial = request.user.employee.name
    if request.method == 'POST':
        form = OfficeExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Office expense record has been created succesfully'))
            return render(request, "close_popup.html")
        else:
            context = {
                "form": form
            }
            return render(request, "popup_forms/office_expense_form.html", context)

    context = {
        "form": form
    }

    return render(request, "popup_forms/office_expense_form.html", context)

def office_expenses_list(request):
    expenses = OfficeExpense.objects.filter(company = request.user.employee.company).order_by("-date")


    context = {
        "expenses": expenses
    }
    return render(request, "office_expense_list.html", context)

@login_required()
def print_withdrawl_voucher_office(request,transaction_id):
    transaction = OfficeExpense.objects.get(company=request.user.employee.company, id=transaction_id)
    context = {
        "transaction": transaction

    }
    return render(request, "print/office_expense_print.html", context)

def treasury(request):
    company = request.user.employee.company
    office_expenses = OfficeExpense.objects.filter(company = company)
    general_transactions = CompanyTreasuryTransaction.objects.filter(company = company, transaction_for = 'general')
    salary_transactions = CompanyTreasuryTransaction.objects.filter(company = company, transaction_for = 'salary')

    context = {
        "company": company,
    "office_expenses": office_expenses,
    "general_transactions": general_transactions,
    "salary_transactions": salary_transactions,



    }
    return render(request, 'treasury.html', context)

@login_required()
def treasury_collect_payment(request):
    form = TreasuryCollectPayment()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['received_by'].initial = request.user.employee.name
    form.fields['transaction_type'].initial = "c"

    if request.method == 'POST':
        form = TreasuryCollectPayment(request.POST)
        if form.is_valid():
            if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    messages.success(request, _('Amount has been credited to treasury.'))
                    return render(request, "close_popup.html")
            else: 

                context = {
                    "form": form,
                    'otp_error': _("Wrong token")
                }

                return render(request, "popup_forms/collect_payment.html", context)
        else:
            context = {
                "form": form
            }
            return render(request, "popup_forms/collect_payment.html", context)

    context = {
        "form": form
    }

    return render(request, "popup_forms/collect_payment.html", context)

@login_required()
def print_agent_reciept_voucher_report(request, agent_id):
    agent = Agent.objects.get(company=request.user.employee.company.id, id=agent_id)
    from_date = request.GET.get('date_min') or None
    to_date = request.GET.get('date_max') or None
    if from_date != None and to_date != None:
        main_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['c'], date__gte = from_date, date__lte = to_date, is_settlement_transaction = False).order_by('date')
        total_amount = 0.00
        total_visas = 0
        total_visas_amount = 0.00
        for t in main_transactions:
            total_amount += float(t.amount)


        
        debit_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['d'], date__gte = from_date, date__lte = to_date).order_by('date')

        for t in debit_transactions:
            total_visas_amount += float(t.amount)
            if t.voucher:
                total_visas += t.voucher.pax


        print_date = datetime.datetime.now()
        context = {
            "agent" : agent,
            "transactions": main_transactions,
            "total_amount": total_amount,
            "total_visas": total_visas,
            "total_visas_amount" : total_visas_amount,
            "print_date": print_date,


            
        }
        return render(request, "print/print_receipt_vouchers_report.html", context)
    else:
        messages.error(request, _("Please enter valid dates"))
        return HttpResponseRedirect(reverse('agent_account_view', kwargs={'agent_id':agent_id, 'agent_type': 'sub_agent'}))
    
@login_required()
def print_agent_account_statement(request, agent_id):
    agent = Agent.objects.get(company=request.user.employee.company.id, id=agent_id)
    from_date = request.GET.get('date_min') or None
    to_date = request.GET.get('date_max') or None
    if from_date != None and to_date != None:
        main_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['c', 'd'], date__gte = from_date, date__lte = to_date).order_by('date')
        total_amount_credit = 0.00
        total_amount_debit = 0.00

        total_visas = 0
        total_visas_amount = 0.00
        for t in main_transactions:
            if t.transaction_type == "c":
                total_amount_credit += float(t.amount)
            elif t.transaction_type == "d":
                total_amount_debit += float(t.amount)
            else:
                pass

    


        
        debit_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['d'], date__gte = from_date, date__lte = to_date).order_by('date')

        for t in debit_transactions:
            total_visas_amount += float(t.amount)
            if t.voucher:
                total_visas += t.voucher.pax

        balance = total_amount_credit - total_amount_debit
        old_account_balance = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, agent__id = agent_id, transaction_type__in = ['c', 'd'], date__lt = from_date).order_by('date')
        old_balance = 0.00
        for t in old_account_balance:
            if t.transaction_type == "c":
                old_balance += float(t.amount)
            elif t.transaction_type == "d":
                old_balance -= float(t.amount)
            else:
                pass
        transactions = []
        account_balance = old_balance
        for t in main_transactions:
            if t.transaction_type == "c":
                account_balance += float(t.amount)
            elif t.transaction_type == "d":
                account_balance -= float(t.amount)
            else:
                pass
            t.balance = account_balance
            transactions.append({
                "transaction": t,
                "balance": account_balance
            })


        print_date = datetime.datetime.now()
        context = {
            "agent" : agent,
            "total_amount_credit": total_amount_credit,
            "total_amount_debit": total_amount_debit,
            "total_visas": total_visas,
            "total_visas_amount" : total_visas_amount,
            "print_date": print_date,
            "balance": balance,
            "transactions": transactions,


            
        }
        return render(request, "print/print_agent_account_statement.html", context)
    else:
        messages.error(request, _("Please enter valid dates"))
        return HttpResponseRedirect(reverse('agent_account_view', kwargs={'agent_id':agent_id, 'agent_type': 'sub_agent'}))

@login_required()
def print_all_agents_reciept_voucher_report(request):
    
    from_date = request.GET.get('date_min') or None
    to_date = request.GET.get('date_max') or None

    if from_date != None and to_date != None:

        main_transactions = AgentPaymentTransaction.objects.filter(company = request.user.employee.company.id, transaction_type__in = ['c'], date__gte = from_date, date__lte = to_date, is_settlement_transaction = False).order_by('date')
        total_amount = 0.00
        total_visas = 0
        total_visas_amount = 0.00
        for t in main_transactions:
            total_amount += float(t.amount)


        context = {
            "transactions": main_transactions,
            "total_amount": total_amount,
            "total_visas": total_visas,
            "total_visas_amount" : total_visas_amount,
        }
        return render(request, "print/print_receipt_vouchers_report.html", context)
    else:
        messages.error(request, _("Please enter valid dates"))
        return HttpResponseRedirect(reverse('payments_agents_list'))

@login_required()
def payroll_list(request):
    payrolls = Payroll.objects.filter(company = request.user.employee.company)


    context = {
        'payrolls': payrolls
    }
    return render(request, 'payrolls.html', context )

@login_required()
def payroll_form(request):
    form = PayrollForm()
    form.fields['company'].initial = request.user.employee.company.id
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            _form = form.save()
            _form

            # Create Salary Slip for every active employee
            employees = Employee.objects.filter(company = request.user.employee.company, is_active=True)
            for e in employees:
                es = EmployeeSalary()
                es.company = request.user.employee.company
                es.payroll = _form
                es.employee = e
                es.salary = e.salary
                es.save()
            messages.success(request, _('New payroll has been created.'))
            return render(request, "close_popup.html")
        else:
            context = {
                "form": form
            }
            return render(request, "popup_forms/payroll_form.html", context)

    context = {
        "form": form
    }

    return render(request, "popup_forms/payroll_form.html", context)

@login_required()
def view_payroll(request, payroll_id):
    payroll = Payroll.objects.get(company = request.user.employee.company, id= payroll_id)
    employees = EmployeeSalary.objects.filter(company = request.user.employee.company, payroll = payroll)

    context = {
        "payroll": payroll,
        "employees": employees
    }
    return render(request, 'payroll_view.html', context)


@login_required()
def print_payslip(request, payroll_id, employee):
    payroll = Payroll.objects.get(company = request.user.employee.company, id= payroll_id)
    payslip = EmployeeSalary.objects.get(company = request.user.employee.company, payroll = payroll, id=employee)

    context = {
        "payroll": payroll,
        "payslip": payslip
    }
    return render(request, 'print/payslip.html', context)

def salary_collected(request, payroll_id, employee):
    payroll = Payroll.objects.get(company = request.user.employee.company, id= payroll_id)
    payslip = EmployeeSalary.objects.get(company = request.user.employee.company, payroll = payroll, id=employee, status="pending")
    if request.method == "POST":
        t_transaction = CompanyTreasuryTransaction()
        t_transaction.company = payslip.company
        t_transaction.transaction_for = 'salary'
        t_transaction.transaction_type = 'd'
        t_transaction.amount = payslip.net_salary()
        t_transaction.payment_by = _('c')
        t_transaction.reason = _('Salary')
        t_transaction.date = payslip.payroll.end_date
        t_transaction.time = datetime.datetime.now()

        t_transaction.performed_by = request.user.employee.name
        t_transaction.received_by = payslip.employee.name
        t_transaction.save()

        payslip.status = 'collected'
        payslip.save()
        messages.success(request, _('Salary for this employee has been marked as Collected.'))
        return HttpResponseRedirect(reverse('view_payroll', kwargs={'payroll_id':payroll_id}))

@login_required()
def treasury_report(request):
    
    from_date = request.GET.get('date_min') or None
    to_date = request.GET.get('date_max') or None

    if from_date != None and to_date != None:

        main_transactions = CompanyTreasuryTransaction.objects.filter(company = request.user.employee.company.id,  date__gte = from_date, date__lte = to_date).order_by('date')
        total_amount_deposit = 0.00
        total_salaries = 0.00
        total_expenses = 0.00
        total_debit = 0.00
        total_credit = 0.00

        for t in main_transactions:
            if t.transaction_type == 'c':
                total_amount_deposit += float(t.amount)
                total_credit += float(t.amount)
            elif t.transaction_type == 'd':
                if t.transaction_for == 'salary':
                    total_salaries += float(t.amount)
                    total_debit += float(t.amount)
                elif t.transaction_for == 'company_expense':
                    total_expenses += float(t.amount)
                    total_debit += float(t.amount)
            else:
                pass
        print_date = datetime.datetime.now()
        context = {
            "transactions": main_transactions,
            "total_amount_deposit": total_amount_deposit,
            "total_salaries": total_salaries,
            "total_expenses" : total_expenses,
            "total_debit" : total_debit,
            "total_credit" : total_credit,
            "print_date": print_date,


        }
        return render(request, "print/print_treasury_report.html", context)
    else:
        messages.error(request, _("Please enter valid dates"))
        return HttpResponseRedirect(reverse('treasury'))
    
@login_required()
def delete_transaction(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        transaction = AgentPaymentTransaction.objects.get(id=transaction_id, company=request.user.employee.company)
        if transaction.voucher != None:
            messages.error(request, _('You cannot delete this transaction as it is linked to a voucher.'))
            return render(request, "close_popup.html")
        else:
            transaction.delete()
            messages.success(request, _('Transaction has been deleted succesfully'))
            return render(request, "close_popup.html")
    else:
        messages.error(request, _('Invalid request'))
        return render(request, "close_popup.html")

@login_required()
def agents_current_balance_print(request):
    company = request.user.employee.company
    agents = Agent.objects.filter(company = company)

    context = {
        "agents": agents,
        "print_date": datetime.datetime.now()
    }
    return render(request, "print/agents_current_balance_print.html", context)

@login_required()
def account_list(request):
    accounts = Account.objects.filter(company = request.user.employee.company)

    context = {
        "accounts": accounts
    }
    return render(request, "accounts_list.html", context)

@login_required()
def account_form(request):
    form = AccountForm()
    form.fields['company'].initial = request.user.employee.company.id
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Account has been created succesfully'))
            return render(request, "close_popup.html")
        else:
            context = {
                "form": form
            }
            return render(request, "popup_forms/account_form.html", context)

    context = {
        "form": form
    }

    return render(request, "popup_forms/account_form.html", context)

@login_required()
def edit_account(request, account_id):
    _id = account_id
    account = Account.objects.get(id=_id, company=request.user.employee.company)
    form = AccountForm(instance=account)
    form.fields['company'].initial = request.user.employee.company.id
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, _('Account has been updated succesfully'))
            return render(request, "close_popup.html")
        else:
            context = {
                "form": form
            }
            return render(request, "popup_forms/account_form_edit.html", context)

    context = {
        "form": form
    }

    return render(request, "popup_forms/account_form.html", context)

# @login_required()
# def account_view(request, account_id):
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     transactions = AccountTransaction.objects.filter(account=account).order_by('-date', '-id')
#     balance = account.balance()
#     _transacions = []
#     for t in transactions:
#         if t.credit == 0.00:
#             _transacions.append({
#                 "t": t,
#                 "balance": balance
#             })
#             balance += float(t.debit)

#         elif t.debit == 0.00:
#             _transacions.append({
#                 "t": t,
#                 "balance": balance
                
#             })
#             balance -= float(t.credit)

#         else:
#             pass

#     context = {
#         "account": account,
#         "transactions": _transacions,
        
#     }
#     return render(request, "account_view.html", context)

# @login_required()
# def transfer_to_account(request, account_id):
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     form = AccountForm(instance=account)
#     form.fields['company'].initial = request.user.employee.company.id
#     form.fields['account_type'].initial = 't'
#     if request.method == 'POST':
#         form = AccountForm(request.POST, instance=account)
#         if form.is_valid():
#             form.save()
#             messages.success(request, _('Amount has been transferred to account succesfully'))
#             return render(request, "close_popup.html")
#         else:
#             context = {
#                 "form": form
#             }
#             return render(request, "popup_forms/account_form.html", context)

#     context = {
#         "form": form
#     }

#     return render(request, "popup_forms/account_form.html", context)

# @login_required()
# def account_transfer_form(request, account_id):
#     form = AccountTransferForm()
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     form.fields['company'].initial = request.user.employee.company.id
#     form.fields['account'].initial = account
#     accounts = Account.objects.filter(company=request.user.employee.company).exclude(id=account_id)
#     form.fields['transfer_to'].queryset = accounts
#     form.fields['date'].initial = datetime.datetime.now()
#     form.fields['debit'].initial = 0.00
#     if request.method == 'POST':
#         form = AccountTransferForm(request.POST)
#         if form.is_valid():
#             if verify_auth_key(request, otp=request.POST.get('token')) == True:
#                     form.save()
#                     messages.success(request, _('Amount has been transferred to account succesfully'))
#                     return render(request, "close_popup.html")
#             else:

#                 context = {
#                     "account": account,

#                     "form": form,
#                     'otp_error': _("Wrong token")
#                 }

#                 return render(request, "popup_forms/account_transfer_form.html", context)
#         else:
#             context = {
#                 "account": account,

#                 "form": form
#             }
#             return render(request, "popup_forms/account_transfer_form.html", context)

#     context = {
#         "account": account,
#         "form": form
#     }

#     return render(request, "popup_forms/account_transfer_form.html", context)

# @login_required()
# def account_credit_form(request, account_id):
#     form = AccountTransactionCreditForm()
#     form.fields['company'].initial = request.user.employee.company.id
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     form.fields['account'].initial = account.id
#     form.fields['date'].initial = datetime.datetime.now()
#     form.fields['performed_by'].initial = request.user.employee.name
#     if request.method == 'POST':
#         form = AccountTransactionCreditForm(request.POST)
#         if form.is_valid():
#             if verify_auth_key(request, otp=request.POST.get('token')) == True:
#                     form.save()
#                     messages.success(request, _('Amount has been credited to account succesfully'))
#                     return render(request, "close_popup.html")
#             else:

#                 context = {
#                     "account": account,
#                     "form": form,
#                     'otp_error': _("Wrong token")
#                 }

#                 return render(request, "popup_forms/account_credit_form.html", context)
#         else:
#             context = {
#                 "account": account,

#                 "form": form
#             }
#             return render(request, "popup_forms/account_credit_form.html", context)
    

#     context = {
#         "account": account,
#         "form": form
#     }

#     return render(request, "popup_forms/account_credit_form.html", context)


# @login_required()
# def account_debit_form(request, account_id):
#     form = AccountTransactionDebitForm()
#     form.fields['company'].initial = request.user.employee.company.id
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     form.fields['account'].initial = account.id
#     form.fields['date'].initial = datetime.datetime.now()
#     form.fields['performed_by'].initial = request.user.employee.name
#     if request.method == 'POST':
#         form = AccountTransactionDebitForm(request.POST)
#         if form.is_valid():
#             if verify_auth_key(request, otp=request.POST.get('token')) == True:
#                     form.save()
#                     messages.success(request, _('Amount has been debited from account succesfully'))
#                     return render(request, "close_popup.html")
#             else:

#                 context = {
#                     "account": account,
#                     "form": form,
#                     'otp_error': _("Wrong token")
#                 }

#                 return render(request, "popup_forms/account_debit_form.html", context)
#         else:
#             context = {
#                 "account": account,

#                 "form": form
#             }
#             return render(request, "popup_forms/account_debit_form.html", context)

#     context = {
#         "account": account,
#         "form": form
#     }

#     return render(request, "popup_forms/account_debit_form.html", context)


# @login_required()
# def print_account_transaction(request, account_id,transaction_id):
#     account = Account.objects.get(id=account_id, company=request.user.employee.company)
#     transaction = AccountTransaction.objects.get(id=transaction_id, company=request.user.employee.company)
#     context = {
#         "account": account,
#         "transaction": transaction
#     }
#     return render(request, "print/print_account_transaction.html", context)


@login_required()
def agent_settlement_credit(request, agent_id):
    agent = Agent.objects.get(id=agent_id, company=request.user.employee.company)
    form = AgentSettlementTransactionCreditForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['agent'].initial = agent.id
    form.fields['date'].initial = datetime.datetime.now()
    form.fields['performed_by'].initial = request.user.employee.name
    if request.method == 'POST':
        form = AgentSettlementTransactionCreditForm(request.POST)
        if form.is_valid():
            if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    is_settled = AgentPaymentTransaction.objects.get(pk=form.instance.pk)
                    is_settled.is_settlement_transaction = True
                    is_settled.save()
                    messages.success(request, _('Amount has been credited to agent succesfully'))
                    return render(request, "close_popup.html")
            else:

                context = {
                    "agent": agent,
                    "form": form,
                    'otp_error': _("Wrong token")
                }

                return render(request, "popup_forms/agent_settlement_form.html", context)
        else:
            context = {
                "agent": agent,

                "form": form
            }
            return render(request, "popup_forms/agent_settlement_form.html", context)
    
    context = {
        "agent": agent,
        "form": form,
        "type": _("Credit")
    }
    return render(request, "popup_forms/agent_settlement_form.html", context)


@login_required()
def agent_settlement_debit(request, agent_id):
    agent = Agent.objects.get(id=agent_id, company=request.user.employee.company)
    form = AgentSettlementTransactionDebitForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['agent'].initial = agent.id
    form.fields['performed_by'].initial = request.user.employee.name
    if request.method == 'POST':
        form = AgentSettlementTransactionDebitForm(request.POST)
        if form.is_valid():
            if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    is_settled = AgentPaymentTransaction.objects.get(pk=form.instance.pk)
                    is_settled.is_settled = True
                    is_settled.save()

                    messages.success(request, _('Amount has been debited from agent succesfully'))
                    return render(request, "close_popup.html")
            else:

                context = {
                    "agent": agent,
                    "form": form,
                    'otp_error': _("Wrong token")
                }

                return render(request, "popup_forms/agent_settlement_form.html", context)
        else:
            context = {
                "agent": agent,

                "form": form
            }
            return render(request, "popup_forms/agent_settlement_form.html", context)
    context = {
        "agent": agent,
        "form": form,
        "type": _("Debit")
    }
    return render(request, "popup_forms/agent_settlement_form.html", context)
        


@login_required()
def edit_agent_settlement(request, agent_id, transaction_id, type):
    agent = Agent.objects.get(id=agent_id, company=request.user.employee.company)
    if type == "c":
        transaction = AgentPaymentTransaction.objects.get(id=transaction_id, company=request.user.employee.company)
        form = AgentSettlementTransactionCreditForm(instance=transaction)
        form.fields['company'].initial = request.user.employee.company.id
        form.fields['agent'].initial = agent.id
        form.fields['performed_by'].initial = request.user.employee.name
        if request.method == 'POST':
            form = AgentSettlementTransactionCreditForm(request.POST, instance=transaction)
            if form.is_valid():
                if verify_auth_key(request, otp=request.POST.get('token')) == True:
                        form.save()
                        messages.success(request, _('Amount has been credited to agent succesfully'))
                        return render(request, "close_popup.html")
                else:

                    context = {
                        "agent": agent,
                        "form": form,
                        'otp_error': _("Wrong token")
                    }

                    return render(request, "popup_forms/agent_settlement_form.html", context)
            else:
                context = {
                    "agent": agent,

                    "form": form
                }
                return render(request, "popup_forms/agent_settlement_form.html", context)
        
        context = {
            "agent": agent,
            "form": form,
            "type": _("Credit")
        }
        return render(request, "popup_forms/agent_settlement_form.html", context)
    elif type == "d":
        transaction = AgentPaymentTransaction.objects.get(id=transaction_id, company=request.user.employee.company)
        form = AgentSettlementTransactionDebitForm(instance=transaction)
        form.fields['company'].initial = request.user.employee.company.id
        form.fields['agent'].initial = agent.id
        form.fields['performed_by'].initial = request.user.employee.name
        if request.method == 'POST':
            form = AgentSettlementTransactionDebitForm(request.POST, instance=transaction)
            if form.is_valid():
                if verify_auth_key(request, otp=request.POST.get('token')) == True:
                        form.save()
                        messages.success(request, _('Amount has been debited from agent succesfully'))
                        return render(request, "close_popup.html")
                else:

                    context = {
                        "agent": agent,
                        "form": form,
                        'otp_error': _("Wrong token")
                    }
        context = {
            "agent": agent,
            "form": form,
            "type": _("Debit")
        }
        return render(request, "popup_forms/agent_settlement_form.html", context)
    
def account_settlement_credit(request, account_id):
    account = Account.objects.get(id=account_id, company=request.user.employee.company)
    form = AccountSettlementTransactionCreditForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['account'].initial = account.id
    form.fields['date'].initial = datetime.datetime.now()
    form.fields['performed_by'].initial = request.user.employee.name
    if request.method == 'POST':
        form = AccountSettlementTransactionCreditForm(request.POST)
        if form.is_valid():
            if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    is_settled = AccountTransaction.objects.get(pk=form.instance.pk)
                    is_settled.is_settlement_transaction = True
                    is_settled.save()
                    messages.success(request, _('Amount has been credited to account succesfully'))
                    return render(request, "close_popup.html")
            else:

                context = {
                    "account": account,
                    "form": form,
                    'otp_error': _("Wrong token")
                }

                return render(request, "popup_forms/account_settlement_form.html", context)
        else:
            context = {
                "account": account,

                "form": form
            }
            return render(request, "popup_forms/account_settlement_form.html", context)
    
    context = {
        "account": account,
        "form": form,
        "type": _("Credit")
    }
    return render(request, "popup_forms/account_settlement_form.html", context)

def account_settlement_debit(request, account_id):
    account = Account.objects.get(id=account_id, company=request.user.employee.company)
    form = AccountSettlementTransactionDebitForm()
    form.fields['company'].initial = request.user.employee.company.id
    form.fields['account'].initial = account.id
    form.fields['performed_by'].initial = request.user.employee.name
    if request.method == 'POST':
        form = AccountSettlementTransactionDebitForm(request.POST)
        if form.is_valid():
            if verify_auth_key(request, otp=request.POST.get('token')) == True:
                    form.save()
                    is_settled = AccountTransaction.objects.get(pk=form.instance.pk)
                    is_settled.is_settlement_transaction = True
                    is_settled.save()
                    messages.success(request, _('Amount has been debited from account succesfully'))
                    return render(request, "close_popup.html")
            else:

                context = {
                    "account": account,
                    "form": form,
                    'otp_error': _("Wrong token")
                }

                return render(request, "popup_forms/account_settlement_form.html", context)
        else:
            context = {
                "account": account,

                "form": form
            }
            return render(request, "popup_forms/account_settlement_form.html", context)
    
    context = {
        "account": account,
        "form": form,
        "type": _("Debit")
    }
    return render(request, "popup_forms/account_settlement_form.html", context)