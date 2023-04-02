from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import *


@user_passes_test(lambda u: u.is_superuser)
def administration_site(request):
    return render(request, 'administration/administration.html')

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    return render(request, 'administration/administration.html')

@user_passes_test(lambda u: u.is_superuser)
def exceptions(request):
    return render(request, 'administration/administration.html')

@user_passes_test(lambda u: u.is_superuser)
def messages(request):
    return render(request, 'administration/administration.html')

@user_passes_test(lambda u: u.is_superuser)
def excercises(request):
    return render(request, 'administration/administration.html')
