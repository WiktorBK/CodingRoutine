from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes

from .tokens import email_verification_token

class Newsletter_User(models.Model):

    email = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def generate_verification_email(self, request):
        mail_subject = "Verify your email address"
        message = render_to_string('base/email_templates/template_verification_email.html', 
            {
            'domain': get_current_site(request).domain,
            'uid':  urlsafe_base64_encode(force_bytes(self.id)),
            'token': email_verification_token.make_token(self),
            'protocol': 'https' if request.is_secure() else 'http'
            })
        email = EmailMessage(mail_subject, message, to = [self.email])

        return email

    def send_daily_coding_excercise(self, request):
        pass

    def generate_welcoming_email(self, request):
        mail_subject = "Welcome on board!"
        message = render_to_string('base/email_templates/template_welcome_email.html')
        email = EmailMessage(mail_subject, message, to = [self.email])
        return email


    class Meta: ordering = ['-created']
    def __str__(self): return self.email
    


class Message_contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    email_contact = models.CharField(max_length=200)
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


    class Meta: ordering = ['-sent']
    def __str__(self): return self.message


class CodingExcercise(models.Model):
    title =  models.CharField(max_length=100, null=True)
    level = models.CharField(max_length=15)
    example_input = models.CharField(max_length=200, null=True)
    example_output = models.CharField(max_length=200, null=True)
    body =  models.CharField(max_length=500)
    
    def __str__(self): return self.body
