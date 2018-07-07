from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponseRedirect, HttpResponse
from redirect_urls import redirect
from .models import UserBase
from .forms import SignUp
from datetime import date
import random, string, logging, requests

# Create your views here.
def index(request):
	return render(request,'sign_and_auth/login.html')

def checkLogin(request):
	try:
		db_object = UserBase.objects.get(email_address = request.POST.get("u_name"), pk = request.POST.get("p_word"))
		user_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
		requests.post('https://textbelt.com/text', {
		  'phone': db_object.tel_number,
		  'message': 'Hello world',
		  'key': 'textbelt',
		})
		return render(request,'sign_and_auth/phone_code.html', {'usercode':user_code})

	except UserBase.DoesNotExist:
		return render(request,'sign_and_auth/login.html', {'error':"Wrong username or password"})

	except UserBase.MultipleObjectsReturned:
		return render(request,'error')

	

def getAccount(request):
	sign_form = SignUp()
	return render(request,'sign_and_auth/get_account.html',{'sign_form':sign_form})


def signUpData(request):
	account_sid = "ACca1e2389846e0178b31504acecc509bb"
	auth_token = "9763e6548acde0a32e46bb070c544859"
	
	#==============================assign form data to user object===========================#

	userObj = UserBase()
	userObj.user_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
	userObj.first_name = request.POST.get("first_name")
	userObj.other_names = request.POST.get("other_names")
	userObj.gender = request.POST.get("gender")
	userObj.email_address = request.POST.get("email")
	userObj.tel_number = str(request.POST.get("country_code")) + str(request.POST.get("telephone"))

	#===========generate code and send it to telephone in message===========================#

	
	user_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
	requests.post('https://textbelt.com/text', {
	  'phone': userObj.tel_number,
	  'message': 'Hello world',
	  'key': 'textbelt',
	})
	#client = Client(account_sid,auth_token)
	#message = client.messages.create(to = userObj.tel_number, from_ = "+15005550006", body = user_code)
	logging.debug(user_code)
	
	#=============================save object after===========================================#
	userObj.save()

	return render_to_response('sign_and_auth/phone_code.html',{'usercode':user_code, 'u_email':userObj.email_address, 'telephone':userObj.tel_number})


@csrf_exempt
def finishSignUp(request):
	send_address = request.POST.get("email")
	userObjData = UserBase.objects.get(email_address = send_address, tel_number = request.POST.get("telephone"))
	
	email_sent = email_send(userObjData.user_id, "Password", userObjData.email_address)

	if (email_sent == 0):
		return render(request, 'error')
	else:
		return render_to_response('sign_and_auth/final_login.html')

def email_send(s_message,s_subject,s_list):
    subject = s_subject
    message = s_message
    email_from = "App_test"
    recipient_list = []
    recipient_list.append(s_list)
    recipient_list.append('obedkasule@gmail.com')
    sent_mails = send_mail( subject, message, settings.EMAIL_HOST_USER, recipient_list )
    return sent_mails

def errorPage(request):
	return render(request, 'sign_and_auth/error.html')


