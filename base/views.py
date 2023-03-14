from django.shortcuts import render, redirect


def home(request):
    context = {}
    return render(request, "base/home.html", context)

def contact(request):
    context = {}
    return render(request, 'base/contact-page.html', context)

def email_verification(request):
    context = {}
    return render(request, 'base/email-verification.html', context)

def thankyou_page(request):
    context = {}
    return render(request, 'base/thankyou-page.html', context)