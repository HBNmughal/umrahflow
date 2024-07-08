
import pyotp
import time
from umrahflow import settings
import datetime



# def auth_key_alternative(username, password):
#     try:
#         user = User.objects.get(username=username)
#         if user.check_password(password):
#             return True
#         else:
#             return False
#     except:
#         return False



def verify_auth_key(request, otp):

    totp = pyotp.TOTP(request.user.employee.token)
    
    if totp.verify(otp) == False:
        if totp.verify(otp, for_time=(datetime.datetime.now()-datetime.timedelta(seconds=30))) == False:
            if totp.verify(otp, for_time=(datetime.datetime.now()+datetime.timedelta(seconds=30))) == False:
                return False
            else:
                return True
        else:
            return True
    else:
        return True
    
def verify_auth_key_login_page(request,user, user_type, otp):

    if user_type == 'employee':
        totp = pyotp.TOTP(user.employee.token)
    elif user_type == 'agent':
        totp = pyotp.TOTP(user.agent.token)
    elif user_type == 'mandoob':
        totp = pyotp.TOTP(user.mandoob.token)
    if totp.verify(otp) == False:
        if totp.verify(otp, for_time=(datetime.datetime.now()-datetime.timedelta(seconds=30))) == False:
            if totp.verify(otp, for_time=(datetime.datetime.now()+datetime.timedelta(seconds=30))) == False:
                return False
            else:
                return True
        else:
            return True
    else:
        return True
        

    #     if settings.DEBUG:
    #     return True
    # else:
    #     totp = pyotp.TOTP(request.user.employee.token)
        
    #     if totp.verify(otp) == False:
    #         time.sleep(5)
    #         if totp.verify(otp) == False:
    #             time.sleep(5)
    #             if totp.verify(otp) == False:
    #                 time.sleep(5)
    #                 return False
    #             else:
    #                 return True
    #         else:
    #             return True   
    #     else:
    #         return True
        
