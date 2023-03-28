from .models import Newsletter_User, ExceptionTracker

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


'''
Sending coding excercise to each user individually according to excercise's order

Email will be sent everyday at 8 am.

'''

def send_excercise():
    users = Newsletter_User.objects.filter(verified=True)
    
    for user in users: 
        excercise = user.generate_daily_coding_excercise()

        # Add exception if there are no excercises in database
        if excercise is None: return ExceptionTracker.objects.create(title="Daily email wasn't sent", exception=f"No excercise for {user.email}")
            

        mail_subject = f"Coding Excercise - {excercise.level} [#{user.excercises_received + 1}]"
        message = render_to_string('base/email_templates/template_excercise.html',{"excercise": excercise})
        email = EmailMessage(mail_subject, message, to=[user.email])
     
        try:
            email.send()
        except Exception as e:
            ExceptionTracker.objects.create(title=f"Failed to send excercise email to {user.email}", exception=e)
