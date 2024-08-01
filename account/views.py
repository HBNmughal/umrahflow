from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account, JournalEntry, ReceiptVoucher, PaymentVoucher, Transaction, delete_allowed, edit_allowed
from .forms import AccountForm, ReceiptVoucherForm,  TransactionForm, LedgerEntryFormSet, PaymentVoucherForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from transport.models import TransportCompany
import datetime
from django.http import HttpResponseRedirect
from agent.models import Agent
from django.db.models import Q
from decimal import Decimal
from django.core.exceptions import ValidationError
from company.models import SystemSettings, Company
from company.forms import AccountsSettingsForm


# @login_required
# def account_create_view(request):
#     if request.method == 'POST':
#         form = AccountForm(request.POST)
#         if form.is_valid():
#             account = form.save(commit=False)
#             account.company = request.user.company
#             account.save()
#             return redirect('account-list')
#     else:
#         form = AccountForm(company=request.user.company)
#     return render(request, 'account/account_form.html', {'form': form})


@login_required
def account_list_view(request):
    def get_account_tree():
        accounts = Account.objects.filter(parent_account=None, company=request.user.employee.company)
        tree = []

        def build_tree(node):
            children = Account.objects.filter(parent_account=node, company=request.user.employee.company)
            if children:
                node.children = [build_tree(child) for child in children]
            return node

        for account in accounts:
            tree.append(build_tree(account))

        return tree
    
    
    
    
    return render(request, 'account_list.html', {'account_tree': get_account_tree()})

@login_required
def create_account(request, pk=None):
    if pk:
        parent_account = Account.objects.get(pk=pk)       
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            account.company = request.user.employee.company
            account.save()
            messages.success(request, _('Account Created.'))
            return render(request, "close_popup.html")
    else:
        form = AccountForm(user = request.user)
        form['company'].initial = request.user.employee.company
        parent_account = Account.objects.get(pk=pk)
        form['parent_account'].initial = Account.objects.get(pk=pk)
        form['account_type'].initial = parent_account.account_type
        form['company'].initial = request.user.employee.company 
        if pk:
            form.fields['parent_account'].widget = forms.HiddenInput()
            form.fields['account_type'].widget = forms.HiddenInput()
            
    return render(request, 'form.html', {'form': form})

@login_required
def edit_account(request, pk):
    account = Account.objects.get(pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account, user=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            account.company = request.user.employee.company
            account.save()
            messages.success(request, _('Account Updated.'))
            return render(request, "close_popup.html")
    else:
        form = AccountForm(instance=account, user=request.user)
        form['company'].initial = request.user.employee.company
        form['parent_account'].initial = account.parent_account
        form['account_type'].initial = account.account_type
        form.fields['parent_account'].widget = forms.HiddenInput()
        form.fields['account_type'].widget = forms.HiddenInput()
    return render(request, 'form.html', {'form': form})



@login_required
def transport_company_account_list_view(request):
    companies = TransportCompany.objects.filter(company=request.user.employee.company)
    context = {'companies': companies}
    
    
    
    
    return render(request, 'transport_companies_list.html', {'companies': companies})


@login_required
def account_view(request, pk):
    account = Account.objects.get(pk=pk, company=request.user.employee.company, level=5)
    journal_entries = JournalEntry.objects.filter(account=account, company=request.user.employee.company).order_by('date', 'pk')
    balance = Decimal(0.00)


    agent = False
   

    entries = []
    for entry in journal_entries:
        balance += Decimal(entry.entry_amount())
        entries.append({
            'entry': entry,
            'balance': balance,
        })


    



    context = {'account': account, 'journal_entries': entries, 'agent':agent}
    return render(request, 'account.html', context)



@login_required
def print_receipt_voucher(request, pk):
    voucher = ReceiptVoucher.objects.get(pk=pk, company=request.user.employee.company)
    return render(request, 'print/receipt_voucher.html', {'transaction': voucher})

@login_required
def print_debit_voucher(request, pk):
    voucher = None
    return render(request, 'print/debit_voucher.html', {'transaction': voucher})



@login_required()
def print_account_statement(request, pk):
    account = Account.objects.get(pk=pk, company=request.user.employee.company)
    from_date = request.GET.get('date_min') or None
    to_date = request.GET.get('date_max') or None
    journal_entries = JournalEntry.objects.filter(account=account, company=request.user.employee.company).order_by('date', 'pk')
    balance = Decimal(0.00)

   

    entries = []
    for entry in journal_entries:
        balance += Decimal(entry.entry_amount())
        entries.append({
            'entry': entry,
            'balance': balance,
        })
    total_debit = sum([entry['entry'].debit for entry in entries])
    total_credit = sum([entry['entry'].credit for entry in entries])
    

    context = {'account': account, 'entries': entries, 'from_date': from_date, 'to_date': to_date, 'total_debit': total_debit, 'total_credit': total_credit}
    return render(request, "print/print_account_statement.html", context)
    


@login_required
def transaction_list_view(request):
    transactions = Transaction.objects.filter(company=request.user.employee.company).order_by('-date', '-pk')
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def transaction_view(request, pk):
    transaction = Transaction.objects.get(pk=pk, company=request.user.employee.company)
    journal_entries = JournalEntry.objects.filter(transaction=transaction, company=request.user.employee.company).order_by('date', 'pk')
    return render(request, 'transaction.html', {'transaction': transaction, 'journal_entries': journal_entries})


@login_required
def receipt_voucher_list_view(request):
    vouchers = ReceiptVoucher.objects.filter(company=request.user.employee.company).order_by('-date', '-pk')
    return render(request, 'receipt_voucher_list.html', {'vouchers': vouchers})

@login_required
def receipt_voucher_view(request, pk):
    voucher = ReceiptVoucher.objects.get(pk=pk, company=request.user.employee.company)
    return render(request, 'receipt_voucher.html', {'voucher': voucher})


@login_required
def payment_voucher_list_view(request):
    vouchers = PaymentVoucher.objects.filter(company=request.user.employee.company).order_by('-date', '-pk')
    return render(request, 'payment_voucher_list.html', {'vouchers': vouchers})

@login_required
def payment_voucher_view(request, pk):
    voucher = PaymentVoucher.objects.get(pk=pk, company=request.user.employee.company)
    return render(request, 'payment_voucher.html', {'voucher': voucher})


@login_required
def receipt_voucher_add_view(request):
    if request.method == 'POST':
        form = ReceiptVoucherForm(request.POST, user=request.user)
        try:
            print('1')
            if form.is_valid():
                voucher = form.save(commit=False)
                voucher.company = request.user.employee.company
                voucher.save()
                voucher_id = voucher.pk
                messages.success(request, _('Receipt Voucher has been added.'))
                print('added')
                return redirect('receipt_voucher_edit_view', pk=voucher_id)
            else:
                form = ReceiptVoucherForm(request.POST, user=request.user)
                context = {
                'form': form,
                'title': _('Receipt Voucher'),
                'allow_edit': True
                }
                return render(request, 'receipt_voucher_form.html', context)
        except ValidationError as e:
            print('3')
            print(e)
            messages.error(request, e)
            form = ReceiptVoucherForm(request.POST, user=request.user)
            context = {
            'form': form,
            'title': _('Receipt Voucher'),
            'allow_edit': True
            }
            return render(request, 'receipt_voucher_form.html', context)
    else:
        form = ReceiptVoucherForm(user=request.user)
        form.fields['company'].initial = request.user.employee.company
        form.fields['collected_from'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        form.fields['to_account'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)

        context = {
            'form': form,
            'title': _('Receipt Voucher'),
            'allow_edit': True
        }
        return render(request, 'receipt_voucher_form.html', context)

    

@login_required
def receipt_voucher_edit_view(request, pk):
    voucher = ReceiptVoucher.objects.get(pk=pk)
    delete = delete_allowed(voucher.company, voucher)
    edit = edit_allowed(voucher.company, voucher)
    if request.method == 'POST':
        form = ReceiptVoucherForm(request.POST, instance=voucher, user=request.user)
        try:
            if form.is_valid():
                voucher = form.save(commit=False)
                voucher.company = request.user.employee.company
                voucher.save()
                messages.success(request, _('Receipt Voucher has been updated.'))
                print('updated')
                return redirect('receipt_voucher_list_view')
            else:

                form = ReceiptVoucherForm(request.POST, user=request.user)
                context = {
                'form': form,
                'title': _('Receipt Voucher') + ' ' + str(voucher.pk),
                'allow_edit': True
                }
                messages.error(request, _('Please correct the errors below.'))
                return render(request, 'receipt_voucher_form.html', context)
        except ValidationError as e:
            print(e)
            messages.error(request, e)
            form = ReceiptVoucherForm(request.POST, user=request.user)
            context = {
            'form': form,
            'title': _('Receipt Voucher') + ' ' + str(voucher.pk),
            'allow_edit': True
            }
            if not edit:
                context['allow_edit'] = False
                for field in form.fields:
                    form.fields[field].widget.attrs['disabled'] = True
            return render(request, 'receipt_voucher_form.html', context)
    else:
        form = ReceiptVoucherForm(instance=voucher, user=request.user)
        form.fields['company'].initial = request.user.employee.company
        form.fields['collected_from'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        form.fields['to_account'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        context = {
            'voucher': voucher,
            'form': form,
            'title': _('Receipt Voucher') + ' ' + str(voucher.pk),
            'allow_edit': True
        }
        if not edit:
            context['allow_edit'] = False
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
        return render(request, 'receipt_voucher_form.html', context)
    
@login_required
def payment_voucher_add_view(request):
    if request.method == 'POST':    
        form = PaymentVoucherForm(request.POST, user=request.user)
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.company = request.user.employee.company
            voucher.save()
            voucher_id = voucher.pk
            messages.success(request, _('Payment Voucher has been added.'))
            return redirect('payment_voucher_edit_view', pk=voucher_id)
        else:
            form = PaymentVoucherForm(request.POST, user=request.user)
            context = {
            'form': form,
            'title': _('Payment Voucher'),
            'allow_edit': True
            }
            return render(request, 'payment_voucher_form.html', context)
            

    else:
        form = PaymentVoucherForm(user=request.user)
        form.fields['company'].initial = request.user.employee.company
        form.fields['paid_to'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        form.fields['from_account'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        context = {
            'form': form,
            'title': _('Payment Voucher'),
            'allow_edit': True
        }

        return render(request, 'payment_voucher_form.html', context)
    

@login_required
def payment_voucher_edit_view(request, pk):
    voucher = PaymentVoucher.objects.get(pk=pk)
    edit = edit_allowed(voucher.company, voucher)
    if request.method == 'POST':
        form = PaymentVoucherForm(request.POST, instance=voucher, user=request.user)
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.company = request.user.employee.company
            voucher.save()
            messages.success(request, _('Payment Voucher has been updated.'))
            return redirect('payment_voucher_list_view')
        else:
            form = PaymentVoucherForm(request.POST, user=request.user)
            context = {
            'form': form,
            'title': _('Payment Voucher') + ' ' + str(voucher.pk),
            'allow_edit': True
            }
            if not edit:
                context['allow_edit'] = False
                for field in form.fields:
                    form.fields[field].widget.attrs['disabled'] = True
            messages.error(request, _('Please correct the errors below.'))
            return render(request, 'payment_voucher_form.html', context)
    else:
        form = PaymentVoucherForm(instance=voucher, user=request.user)
        form.fields['company'].initial = request.user.employee.company
        form.fields['paid_to'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
        form.fields['from_account'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)
    

        context = {
            'voucher': voucher,
            'form': form,
            'title': _('Payment Voucher') + ' ' + str(voucher.pk),
            'allow_edit': True
        }
        if not edit:
            context['allow_edit'] = False
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True

        return render(request, 'payment_voucher_form.html', context)
    

def tempelate_test(request):
    return render(request, 'print/debit_voucher_test.html')


@login_required
def receipt_voucher_print(request, pk):
    voucher = ReceiptVoucher.objects.get(pk=pk)
    return render(request, 'print/receipt_voucher_print.html', {'voucher': voucher})

def payment_voucher_print(request, pk):
    voucher = PaymentVoucher.objects.get(pk=pk)
    return render(request, 'print/payment_voucher_print.html', {'voucher': voucher})

@login_required()
def accounts_settings_form(request):
    company = request.user.employee.company
    settings = SystemSettings.objects.get(company=company)
    form = AccountsSettingsForm(instance=settings, user=request.user)
    if request.method == "POST":
        form = AccountsSettingsForm(request.POST, instance=settings, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Accounts settings have been updated successfully.'))
            return render(request, "close_popup.html")
        else:
            messages.error(request, _('Error while updating accounts settings'))
    context = {
        "form": form,
        "title": _("Accounts Settings")
    }
    return render(request, "form.html", context)

@login_required
def create_transaction(request):
    from company.models import Company
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        ledger_entry_formset = LedgerEntryFormSet(request.POST)
        if transaction_form.is_valid() and ledger_entry_formset.is_valid():
            company = Company.objects.get(pk=request.user.employee.company.pk)
            description_en = transaction_form.cleaned_data['description']
            description_ar = transaction_form.cleaned_data['description']
            reference_no = transaction_form.cleaned_data['reference_no']
            ledger_entries = []
            for form in ledger_entry_formset:
                if form.cleaned_data:
                    ledger_entries.append({
                        'account': form.cleaned_data['account'].id,
                        'transaction_type': 'debit' if form.cleaned_data['debit'] > 0.00 else 'credit',
                        'amount': form.cleaned_data['debit'] if form.cleaned_data['debit'] > 0.00 else form.cleaned_data['credit'],
                        'description_en': form.cleaned_data['description'],
                        'description_ar': form.cleaned_data['description'],
                    })
            
            try:
                transaction = Transaction.objects.create_transaction_with_entries(
                    company=company,
                    description_en=description_en,
                    description_ar=description_ar,
                    reference_no=reference_no,
                    ledger_entries=ledger_entries,
                    date = transaction_form.cleaned_data['date']
                )
                messages.success(request, 'Transaction created successfully!')
                return redirect('transaction_view', pk=transaction.pk)
            except ValidationError as e:
                messages.error(request, e.message)

        

    else:
        transaction_form = TransactionForm()
        ledger_entry_formset = LedgerEntryFormSet()
        # set queryset for account field
    for form in ledger_entry_formset:
        form.fields['account'].queryset = Account.objects.filter(company=request.user.employee.company, level=5)

    return render(request, 'create_transaction.html', {
        'transaction_form': transaction_form,
        'ledger_entry_formset': ledger_entry_formset,
    })


@login_required()
def agents_accounts_view(request, agent_type):
    company = request.user.employee.company
    agents = Agent.objects.filter(company = company, agent_type=agent_type)
    _company = Company.objects.get(id=request.user.employee.company.id)


    if agent_type == 'external':
        page_title = _("External Agent Accounts")
    elif agent_type == 'virtual':
        page_title = _("Virtual Agent Accounts")


    context = {
        "agents": agents,
        "company": _company,
        "page_title": page_title
    }
    return render(request, "agents_accounts_view.html", context)