from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.decorators import user_passes_test

from .forms import MessageContactForm, NewsletterUserForm
from .models import Newsletter_User, Message_contact, ExceptionTracker, CodingExcercise
from .tokens import email_verification_token, unsubscribe_token
from .services import *


def email_verification(request):
    context = {}
    return render(request, 'base/email-verification.html', context=context)

def thankyou_page(request):
    context = {}
    return render(request, 'base/thankyou-page.html', context=context)

def message_sent(request):
    context = {}
    return render(request, 'base/message_sent.html', context=context)

def verify(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = Newsletter_User.objects.get(id=uid)
    except: user = None

    if user and email_verification_token.check_token(user, token): 
        user.verified = True
        user.save()
        welcoming_email = user.generate_welcoming_email()

        try:
            welcoming_email.send()
        except Exception as e: 
            ExceptionTracker.objects.create(title='Failed to send welcoming email', exception=e)

        return redirect('thank-you')
    else:
        return HttpResponse("Error: Activation link is invalid")

def unsubscribe(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = Newsletter_User.objects.get(id=uid)
    except: return HttpResponse("Error: Activation link is invalid")
    
    if user and user.unsubscribe_token == token:
        user.active = False
        user.verified = False
        user.save()
    else: return HttpResponse("Error: Activation link is invalid")

    return render(request, "base/unsubscribe-page.html")

def contact(request):
    form = MessageContactForm()
    if request.method == "POST":
        form = MessageContactForm(request.POST)
        message = create_message(request)

        context = {'form': form, 'first_name': message.first_name, 'sent': True}
        return render(request, "base/message_sent.html", context=context)
    
    context = {'form': form}
    return render(request, 'base/contact-page.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def resend(request, email):
    try: 
        user = Newsletter_User.objects.get(email=email)
        email = user.generate_verification_email(request)
    
        return HttpResponse('Success: verifiaction email has been sent') if email.send() else HttpResponse('Error: Something went wrong')
    except Exception as e: 
        ExceptionTracker.objects.create(title="Failed to resend verification link", exception=e)

def home(request):
    form = NewsletterUserForm()
    context = {'form': form}
    if request.method == "POST":

        form = NewsletterUserForm(request.POST)
        email = request.POST.get('email').lower()  

        try:
            validate_email(email)
            user = Newsletter_User.objects.filter(email=email).first()
            if user:
                verified = user.verified
                context = {'form': form, 'enrolled': True, 'verified': verified, 'email': email, 'active': user.active}
            else:
                new_user = create_user(email)
                verification_email = new_user.generate_verification_email(request)
                return HttpResponseRedirect('email-verification') if verification_email.send() else messages.error("something went wrong")
        except: 
            messages.error(request, "Enter valid email address")

    return render(request, "base/home.html", context=context)

def page_not_found(request, exception, template_name='404.html'):
    
    return render(request, template_name, status=404)

