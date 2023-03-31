from .models import Newsletter_User, ExceptionTracker, Message_contact
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
    first_name = request.POST.get('first_name').capitalize()
    last_name = request.POST.get('last_name').capitalize()
    message = request.POST.get('message')

    message = Message_contact.objects.create(
    email_contact=email, 
    first_name=first_name, 
    last_name=last_name, 
    message=message)

    return message


