# from payment.models import Account  # Import your Account model
from agent.models import Agent
from mandoob.models import Mandoob
from django.contrib.auth.models import User

def account_names(request):
    # Retrieve the account names you want to display
    if request.user.is_authenticated:
        is_agent = Agent.objects.filter(user=request.user).exists()
        is_employee = User.objects.filter(employee__user=request.user).exists()
        if is_agent:
            account_names = Agent.objects.filter(user=request.user)
        elif is_employee:
            account_names = None
        else:
            account_names = Mandoob.objects.filter(user=request.user)

        return {'account_names': account_names}
        
        
    else:
        return {}
    
