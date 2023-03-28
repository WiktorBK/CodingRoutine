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

def home(request):
    form = NewsletterUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = NewsletterUserForm(request.POST)
        email = request.POST.get('email').lower()  
        user = Newsletter_User.objects.get(email=email)

        try:
            validate_email(email)
            try:
                verified = user.verified
                context = {'form': form, 'enrolled': True, 'verified': verified, 'email': email, 'active': user.active}
                
            except:
                user = Newsletter_User.objects.create(email = email)
                user.save()
                verification_email = user.generate_verification_email(request)
                return HttpResponseRedirect('email-verification') if verification_email.send() else messages.error("something went wrong")
        except: 
            messages.error(request, "Enter valid email address")

    return render(request, "base/home.html", context=context)



def contact(request):
    form = MessageContactForm()
    if request.method == "POST":
        form = MessageContactForm(request.POST)
        email = request.POST.get('email_contact').lower()
        first_name = request.POST.get('first_name').capitalize()
        last_name = request.POST.get('last_name').capitalize()
        message = request.POST.get('message')
        
        Message_contact.objects.create(
        email_contact=email, 
        first_name=first_name, 
        last_name=last_name, 
        message=message)
        context = {'form': form, 'first_name': first_name}
        return render(request, "base/message_sent.html", context=context)
    
    context = {'form': form}
    return render(request, 'base/contact-page.html', context=context)

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
    except: user = None


    #  needs change
    if user and email_verification_token.check_token(user, token): 
        user.active = False
        user.verified = False
        user.save()
        

    return render(request, "base/unsubscribe-page.html")

@user_passes_test(lambda u: u.is_superuser)
def resend(request, email):

    try: 
        user = Newsletter_User.objects.get(email=email)
        email = user.generate_verification_email(request)
    
        return HttpResponse('Success: verifiaction email has been sent') if email.send() else HttpResponse('Error: Something went wrong')
    except Exception as e: 
        ExceptionTracker.objects.create(title="Failed to resend verification link", exception=e)



def page_not_found(request, exception, template_name='404.html'):
    
    return render(request, template_name, status=404)

