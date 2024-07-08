from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib import messages #import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
import core.email_settings as settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.token_auth import verify_auth_key_login_page
from agent.models import Agent
from company.models import Employee
from django.contrib.auth.models import User
from mandoob.models import Mandoob
# from mandoob.models import Mandoob




def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)




# Create your views here.
@login_required()
def home(request):
    if Employee.objects.filter(user=request.user).exists():
        return render(request, "dashboard.html")
    elif Agent.objects.filter(user=request.user).exists():
        return render(request, "agent_dashboard.html")
    elif Mandoob.objects.filter(user=request.user).exists():
        return redirect('mandoob')
    



def login_form(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                
            )
            
            if user is not None:
                if Employee.objects.filter(user=user).exists():
                    if verify_auth_key_login_page(request,user=user,user_type="employee", otp=request.POST.get('token')) == True:
                        login(request, user)
                        if user.employee.current_app == None:
                            return redirect('apps')
                        else:
                            return redirect('dashboard')
                    else:
                        messages.error(request, _("Wrong Google Auth Key."))
                        return render(request, 'login.html')
                
                elif Mandoob.objects.filter(user=user).exists():
                    if verify_auth_key_login_page(request,user=user,user_type="mandoob", otp=request.POST.get('token')) == True:
                        login(request, user)
                        return redirect('mandoob_dashboard')
                    else:
                        messages.error(request, _("Wrong Google Auth Key."))
                        return render(request, 'login.html')

                elif Agent.objects.filter(user=user).exists():
                    if verify_auth_key_login_page(request,user=user,user_type="agent", otp=request.POST.get('token')) == True:
                        login(request, user)
                        return redirect('agent_dashboard')
                    else:
                        messages.error(request, _("Wrong Google Auth Key."))
                        return render(request, 'login.html')
                
            else:


                messages.error(request, _("Wrong username or password."))
                return render(request, 'login.html')

        context = {'form': form}
        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout_button(request):
    logout(request)
    return redirect('login')
@login_required()
def close_popup(request):
    return render(request, "close_popup.html")
    




@login_required()
def apps(request):
    return render(request, "apps.html")
    
@login_required()
def apps(request):
    return render(request, "apps.html")
    
def select_app(request, app):
    employee = Employee.objects.get(id = request.user.employee.id)
    employee.current_app = app
    employee.save()
    return redirect('dashboard')