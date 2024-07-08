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

from agent.models import Agent


# create function which returns sale price of agent htmx 
def get_agent_sale_price(request):
    agent_id = request.GET.get('agent')
    agent = Agent.objects.get(id=id)
    return HttpResponse(agent.sale_price)


