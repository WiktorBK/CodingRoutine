from base.models import Newsletter_User, ExceptionTracker, MessageContact, CodingExercise
from .tokens import unsubscribe_token

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import traceback

def create_user(email):
        
        '''
        Create new user with given email and generated unsubscribe token.

        Save to database
        '''
        user = Newsletter_User.objects.create(email = email)
        user.unsubscribe_token = unsubscribe_token.generate_unsubscribe_token(user)
        user.save()
        return user
        
def create_message(request):

    '''
    Get the values from the form

    Create new message object 
    '''
    email = request.POST.get('email_contact').lower()
    fname = request.POST.get('first_name').capitalize()
    lname = request.POST.get('last_name').capitalize()
    message = request.POST.get('message')

    try:    
     message = MessageContact.objects.create(
     email_contact=email, first_name=fname, last_name=lname, message=message)
    except Exception:
     ExceptionTracker.objects.create(title='Failed to create message', exception=traceback.format_exc()) 

    return message


def create_exercise(request):
    
    '''
    Get the values from the form

    Create new coding exercise
    '''
    title = request.POST.get('title').capitalize()
    diff = request.POST.get('difficulty').capitalize()
    body = request.POST.get('body')
    exiput = request.POST.get('example_input')
    exoput = request.POST.get('example_output')
    try:     
     exercise = CodingExercise.objects.create( title=title,difficulty=diff,body=body,example_input=exoput,example_output=exiput)
     return exercise
    except Exception:
     ExceptionTracker.objects.create(title='Failed to create exercise', exception=traceback.format_exc())   
    
    

