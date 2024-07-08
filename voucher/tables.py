from django.urls import reverse
from django.http import JsonResponse
from.models import AgentVoucher, FixedVoucherPrices, TransportInvoice
from django.db.models import Q
from functools import reduce

def server_side_data(request):
    # Process DataTables parameters
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column = request.GET.get('order[0][column]', 0)
    order_direction = request.GET.get('order[0][dir]', 'asc')

    # Define the columns you want to return
    columns = ['voucher_no', 'pax', 'date', 'group_no', 'agent', 'extra_fees', 'voucher_total']

    # Query your data
    data = AgentVoucher.objects.filter(company=request.user.employee.company)

    # Apply filtering
    if search_value:
        filter_conditions = [
            f'{column}__icontains' for column in columns
        ]
        data = data.filter(
            reduce(lambda x, y: x | y, (Q(**{condition: search_value}) for condition in filter_conditions))
        )

    # Apply sorting
    if order_direction == 'asc':
        data = data.order_by(columns[int(order_column)])
    else:
        data = data.order_by(f'-{columns[order_column]}')

    # Get the total count of records before filtering
    total_count = data.count()

    # Get the records for the current page
    data = data[start:start + length]

    # Prepare the data as a list of dictionaries
    data = [
        {
            "voucher_no": item.voucher_no,
            "pax": item.pax,
            "date": item.date,
            "group_no": item.group_no,
            "agent": item.agent.name,
            "extra_fees": item.extra_fees,
            "voucher_total": item.voucher_total,
            "edit_url": reverse('edit_voucher', args=['sub_agent_voucher', item.id]),
            "print_url": reverse('print_voucher', args=['sub_agent_voucher', item.id]),
        }
        for item in data
    ]

    response_data = {
        'draw': 1,
        'recordsTotal': total_count,
        'recordsFiltered': total_count,  # Change this if you implement filtering
        'data': data,
    }

    return JsonResponse(response_data)