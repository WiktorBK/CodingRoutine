from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes

from codingroutine.tokens import email_verification_token
from base.models import Newsletter_User, ExceptionTracker



def send_excercise():
    '''
    Sending coding excercise to each user individually according to excercise's order

    Email will be sent everyday. - Refer to jobs/updater.py

    '''
    users = Newsletter_User.get_verified_users()
    
    for user in users: 
        excercise = user.generate_daily_coding_excercise()

        # Add   exception if there are no excercises in database
        if excercise is None: return ExceptionTracker.objects.create(title="Daily email wasn't sent", exception=f"No excercise for {user.email}")

        mail_subject = f"Coding Excercise - {excercise.difficulty} [#{user.excercises_received + 1}]"
        message = render_to_string('base/email_templates/template_excercise.html',{"excercise": excercise, 'uid':  urlsafe_base64_encode(force_bytes(user.id)),
         'unsubscribe_token': user.unsubscribe_token})
        text_conent = strip_tags(message)
        email = EmailMultiAlternatives(mail_subject, text_conent, to=[user.email])
        email.attach_alternative(message, "text/html")
       
        try:
            email.send()
        except Exception as e:
            ExceptionTracker.objects.create(title=f"Failed to send excercise email to {user.email}", exception=e)

    print('okay')


def send_reminder():
    '''

    Sends a remainder email when user has unverified account.

    Refer to jobs/updater.py
    
    '''
    users = Newsletter_User.objects.filter(active=True, verified=False)
    for user in users:
        
        mail_subject = "Verify your account"
        message = render_to_string(
        'base/email_templates/template_reminder.html',
        {'uid':  urlsafe_base64_encode(force_bytes(user.id)),
        'token': email_verification_token.make_token(user),
        'unsubscribe_token': user.unsubscribe_token})

        email = EmailMessage(mail_subject, message, to=[user.email])
               
        try:
            email.send()
        except Exception as e:
            ExceptionTracker.objects.create(title=f"Failed to send reminder email to {user.email}", exception=e)
                                                

