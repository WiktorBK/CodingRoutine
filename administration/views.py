from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import ExceptionTracker
from base.models import *
from .forms import AddExcerciseForm
from base.functions import create_excercise


@user_passes_test(lambda u: u.is_superuser)
def administration_site(request):
    unread_messages = len(MessageContact.get_unread_messages())
    unread_exceptions = len(ExceptionTracker.get_unread_exceptions())

    context={"unread_messages": unread_messages, "unread_exceptions": unread_exceptions}
    return render(request, 'administration/administration.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_ = Newsletter_User.get_users()

    context={"users": users_, "users_count": len(users_)}
    return render(request, 'administration/users.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def exceptions(request):
    exceptions_ = ExceptionTracker.get_exceptions()
    unread_exceptions = len(ExceptionTracker.get_unread_exceptions())

    context={"exceptions": exceptions_, "unread_count": unread_exceptions, "exceptions_count": len(exceptions_)}
    return render(request, 'administration/exceptions.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def exception(request, eid):
    e=ExceptionTracker.objects.get(id=eid)
    e.make_read()

    context={'exception':e}
    return render(request, 'administration/exception.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def contact_messages(request):
    messages_=MessageContact.get_messages()
    unread_messages = len(MessageContact.get_unread_messages())

    context={"messages": messages_, "unread_count": unread_messages, 'messages_count': len(messages_)}
    return render(request, 'administration/messages.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def message(request, mid):
    m=MessageContact.objects.get(id=mid)
    m.make_read()

    context={'message':m,'message_id': m.id}
    return render(request, 'administration/message.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def delete_message(request, mid):
    try:
     m=MessageContact.objects.get(id=mid)
     m.delete()
    except Exception as e: 
     ExceptionTracker.objects.create(title='Failed to delete message', exception=e)
    return redirect('messages')

@user_passes_test(lambda u: u.is_superuser)
def excercises(request):
    excercises_ = CodingExcercise.get_excercises()

    context={"excercises": excercises_, "excercises_count": len(excercises_)}
    return render(request, 'administration/excercises.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def add_excercise(request):
    form=AddExcerciseForm()

    if request.method == "POST":   
        form = AddExcerciseForm(request.POST)
        excercise = create_excercise(request)
        return redirect('excercises')

    context={'form': form}
    return render(request, 'administration/add_excercise.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def admins(request):
    admins_ = User.objects.filter(is_superuser=True)
    
    context={"admins": admins_, "admins_count": len(admins_)}
    return render(request, 'administration/admins.html', context=context)


def loginPage(request):
    if request.user.is_authenticated: return redirect('administration-site')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('administration-site')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'administration/login.html')

def logoutUser(request):
    logout(request)
    return render(request, 'administration/logout.html')