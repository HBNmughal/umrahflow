from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.db.models import Q
from arrival_voucher.models import ArrivalVoucher
from transport.models import TransportMovement
from .forms import ArrivalVoucherPurchaseInvoiceForm, ArrivalVoucherSaleInvoiceForm, TransportMovementOutsidePackageFormset, TransportMovementIncludedPackageFormset


@login_required()
def arrival_voucher_invoice(request, voucher_id):
    voucher = get_object_or_404(ArrivalVoucher, id=voucher_id, company=request.user.employee.company)
    package_movements = TransportMovement.objects.filter(voucher=voucher, outside_package=False)
    arrival_voucher_purchase_invoice_form = ArrivalVoucherPurchaseInvoiceForm(instance=voucher)
    arrival_voucher_sale_invoice_form = ArrivalVoucherSaleInvoiceForm(instance=voucher)
    transport_formset_included_package = TransportMovementIncludedPackageFormset(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk).exclude(outside_package=True)) or None
    transport_formset_outside_package = TransportMovementOutsidePackageFormset(instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk, outside_package=True)) or None

    if request.method == 'POST':
        arrival_voucher_purchase_invoice_form = ArrivalVoucherPurchaseInvoiceForm(request.POST, instance=voucher)
        arrival_voucher_sale_invoice_form = ArrivalVoucherSaleInvoiceForm(request.POST, instance=voucher)
        transport_formset_outside_package = TransportMovementOutsidePackageFormset(request.POST, instance=voucher, queryset=TransportMovement.objects.order_by('date', 'time').filter(voucher=voucher.pk, outside_package=True))
        voucher.package_purchase_amount = float(request.POST.get('package_purchase_amount') or 0.00)
        voucher.package_sale_amount = float(request.POST.get('package_sale_amount') or 0.00)

        for x in request.POST:
            print(x)

        transport_formset_outside_package.save()
        voucher.accounts_status = 'approved'
        voucher.save()
        messages.success(request, _('Invoice updated successfully'))

        next_voucher = ArrivalVoucher.objects.filter(company=request.user.employee.company, accounts_status='pending').order_by('id').first()
        next_voucher = next_voucher or voucher
        if request.POST.get('next'):
            return HttpResponseRedirect(reverse('arrival_voucher_invoice', args=[next_voucher.pk]))
        else:
            return HttpResponseRedirect(reverse('pending_arrival_voucher_invoice_list'))
        


    print(arrival_voucher_sale_invoice_form.fields['package_sale_amount'].initial)
    arrival_voucher_sale_invoice_form.fields['package_sale_amount'].initial = 5000.00
    print(arrival_voucher_sale_invoice_form.fields['package_sale_amount'].initial)


    sale_form = arrival_voucher_sale_invoice_form

    print(sale_form.fields['package_sale_amount'].initial)
             
        

    context = {
        'voucher': voucher,
        'package_movements': package_movements,
        'arrival_voucher_purchase_invoice_form': arrival_voucher_purchase_invoice_form,
        'arrival_voucher_sale_invoice_form': sale_form,
        'transport_formset_included_package': transport_formset_included_package,
        'transport_formset_outside_package': transport_formset_outside_package,
    }
    return render(request, 'arrival_voucher_invoice.html', context)




@login_required()
def pending_arrival_voucher_invoice_list(request):

    # get all arrival vouchers for the company order by date
    arrival_vouchers = ArrivalVoucher.objects.filter(company=request.user.employee.company, accounts_status='pending').order_by('id')
    context = {
        'arrival_vouchers': arrival_vouchers,
    }
    return render(request, 'pending_arrival_voucher_invoice_list.html', context)


@login_required()
def approved_arrival_voucher_invoice_list(request):

    # get all arrival vouchers for the company order by date
    arrival_vouchers = ArrivalVoucher.objects.filter(company=request.user.employee.company, accounts_status='approved').order_by('id')
    context = {
        'arrival_vouchers': arrival_vouchers,
    }
    return render(request, 'approved_arrival_voucher_invoice_list.html', context)


