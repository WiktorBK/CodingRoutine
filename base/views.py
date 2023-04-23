from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError

from .forms import MessageContactForm, NewsletterUserForm
from .models import Newsletter_User, MessageContact, ExceptionTracker, CodingExcercise
from codingroutine.tokens import email_verification_token, unsubscribe_token
from codingroutine.functions import *



def thankyou_page(request):
    context = {}
    return render(request, 'base/thankyou-page.html', context=context)

def message_sent(request):
    context = {}
    return render(request, 'base/message_sent.html', context=context)

def contact(request):
    form = MessageContactForm()
    if request.method == "POST":
        form = MessageContactForm(request.POST)
        message = create_message(request)
        
        try: fname=message.first_name 
        except: fname=message

        context = {'form': form, 'first_name': fname, 'sent': True}
        return render(request, "base/message_sent.html", context=context)
    
    context = {'form': form}
    return render(request, 'base/contact-page.html', context=context)

def unsubscribe_how_to(request):
    return render(request, "base/unsubscribe-how-to.html")


def home(request):
    form = NewsletterUserForm()
    context = {'form': form}
    if request.method == "POST":

        form = NewsletterUserForm(request.POST)
        email = request.POST.get('email').lower()  

        try:
            validate_email(email)
            user = Newsletter_User.objects.filter(email=email).first()
            if user and user.active == True:
                verified = user.verified
                context = {'form': form, 'enrolled': True, 'verified': verified, 'email': email, 'active': user.active}
            elif user and user.active == False:
                user.active = True
                user.save()
                verification_email = user.generate_verification_email(request)
                return HttpResponseRedirect('email-verification') if verification_email.send() else messages.error("something went wrong")
            else:
                new_user = create_user(email)
                verification_email = new_user.generate_verification_email(request)
                return HttpResponseRedirect('email-verification') if verification_email.send() else messages.error("something went wrong")
        except ValidationError: 
            messages.error(request, "Enter valid email address")

    return render(request, "base/home.html", context=context)

def page_not_found(request, exception, template_name='404.html'):
    
    return render(request, template_name, status=404)
