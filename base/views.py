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
            print("user already exists")
        except:
            Newsletter_User.objects.create(email = email)


    return render(request, "base/home.html", context)

def contact(request):
    form = NewsletterUserForm()
    context = {'form': form}

    return render(request, 'base/contact-page.html', context)

def email_verification(request):
    context = {}
    return render(request, 'base/email-verification.html', context)

def thankyou_page(request):
    context = {}
    return render(request, 'base/thankyou-page.html', context)