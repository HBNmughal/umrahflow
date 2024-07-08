from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
import datetime
from transport.models import TransportMovement
from django.db.models import Q


# Create your views here.

def home(request):
    return redirect('mandoob_operating_schedule')


@login_required()
def mandoob_operating_schedule(request):
    
    mandoob_city = request.user.mandoob.city

    min_date = datetime.date.today() - datetime.timedelta(days=1)
    max_date = datetime.date.today() + datetime.timedelta(days=1)
    
    movements = TransportMovement.objects.filter(voucher__company=request.user.mandoob.company, date__range=[min_date, max_date]).order_by('date', 'time')

    movements = movements.filter(voucher__status='approved', status__in=['confirmed', 'pending', 'on_the_way','delayed'])
    movements = movements.filter(Q(route__mandoob_mark_as_on_the_way=mandoob_city) | Q(route__mandoob_mark_as_completed=mandoob_city))
    context = {
        'movements': movements,
    }
    
    return render(request, "mandoob_operating_schedule.html", context)



