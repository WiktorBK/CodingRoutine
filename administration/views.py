from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from .models import *
from base.models import *


@user_passes_test(lambda u: u.is_superuser)
def administration_site(request):
    unread_messages = len(Message_contact.get_unread_messages())
    unread_exceptions = len(ExceptionTracker.get_unread_exceptions())

   

    context={"unread_messages": unread_messages, "unread_exceptions": unread_exceptions}
    return render(request, 'administration/administration.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_ = Newsletter_User.get_users()

    context={"users": users_}
    return render(request, 'administration/users.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def exceptions(request):
    exceptions_ = ExceptionTracker.get_exceptions()

    context={"exceptions": exceptions_}
    return render(request, 'administration/exceptions.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def messages(request):
    messages_=Message_contact.get_messages()

    context={"messages": messages_}
    return render(request, 'administration/messages.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def excercises(request):
    excercises_ = CodingExcercise.get_excercises()

    context={"excercises": excercises_}
    return render(request, 'administration/excercises.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def admins(request):
    admins_ = User.objects.filter(is_superuser=True)

    context={"admins": admins_}
    return render(request, 'administration/admins.html')