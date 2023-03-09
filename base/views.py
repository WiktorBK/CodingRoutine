from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    context = {}
    return render(request, "base/home.html", context)
