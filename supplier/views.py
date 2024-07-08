from django.shortcuts import render
from supplier.models import Supplier
# Create your views here.



def view_supplier(request):
    suppliers = Supplier.objects.filter(company=request.user.employee.company)
    context = {
        'suppliers': suppliers
    }
    return render(request, 'supplier/view_supplier.html', context)

# def add_supplier(request):
#     if request.method == 'POST':

#     return render(request, 'supplier/add_supplier.html')