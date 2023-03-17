from django.shortcuts import render, redirect
from .forms import MessageContactForm, NewsletterUserForm
from .models import Newsletter_User, Message_contact

def home(request):
    form = NewsletterUserForm()
    context = {'form': form}

    if request.method == "POST":
        form = NewsletterUserForm(request.POST)
        email = request.POST.get('email').lower()
        try:
            user = Newsletter_User.objects.get(email=email)
            print("user already signed up")
        except:
            Newsletter_User.objects.create(email = email)
            return redirect('email-verification')


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