from .models import Newsletter_User, ExceptionTracker, Message_contact, CodingExcercise
from .tokens import unsubscribe_token

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
     message = Message_contact.objects.create(
     email_contact=email, first_name=fname, last_name=lname, message=message)
    except Exception as e:
     ExceptionTracker.objects.create(title='Failed to create message', exception=e) 

    return message


def create_excercise(request):
    
    '''
    Get the values from the form

    Create new coding excercise
    '''
    title = request.POST.get('title').capitalize()
    diff = request.POST.get('difficulty').capitalize()
    body = request.POST.get('body')
    exiput = request.POST.get('example_input')
    exoput = request.POST.get('example_output')
    try:    
     excercise = CodingExcercise.objects.create(
     title=title,difficulty=diff,body=body,example_input=exoput,example_output=exiput)
     return excercise
    except Exception as e:
     ExceptionTracker.objects.create(title='Failed to create excercise', exception=e)   
    
    

