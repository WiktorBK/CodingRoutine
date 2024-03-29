from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import ExceptionTracker
from base.models import *
from .forms import AddExerciseForm, EditExerciseForm
from codingroutine.functions import create_exercise

import traceback

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
    except Exception: 
     ExceptionTracker.objects.create(title='Failed to delete message', exception=traceback.format_exc())
    return redirect('messages')

@user_passes_test(lambda u: u.is_superuser)
def exercises(request):
    exercises_ = CodingExercise.get_exercises()

    context={"exercises": exercises_, "exercises_count": len(exercises_)}
    return render(request, 'administration/exercises.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def add_exercise(request):
    form=AddExerciseForm()

    if request.method == "POST":   
        form = AddExerciseForm(request.POST)
        exercise = create_exercise(request)
        return redirect('exercises')

    context={'form': form}
    return render(request, 'administration/add_exercise.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def edit_exercise(request, eid):

    # context values
    exercise=CodingExercise.objects.get(id=eid)
    form=EditExerciseForm(exercise)


    from base.models import DIFFICULTY_CHOICES
    ''' 
    find difficulties left to choose
    '''
    diff_left = []
    for x, y in DIFFICULTY_CHOICES:
        if y.lower() == exercise.difficulty.lower(): continue
        diff_left.append((x, y))
    
    if request.method == "POST":
        form = EditExerciseForm(request.POST)
        exercise.update_exercise(request)
        return redirect('exercises')
    
    context={"exercise": exercise, "form": form, "difficulties": diff_left}
    return render(request, 'administration/edit_exercise.html', context=context)

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

@user_passes_test(lambda u: u.is_superuser)
def logoutUser(request):
    logout(request)
    return render(request, 'administration/logout.html')