from django.shortcuts import render, redirect
from .forms import MessageContactForm, NewsletterUserForm

def home(request):
    form = NewsletterUserForm()
    context = {'form': form}

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